var local_ingred_set = new Set();
var local_exclude_set = new Set();
var ingredRegex = new RegExp("([?&])ingred_list=.*?(&|$)", "i");
var excludeRegex = new RegExp("([?&])exclude_list=.*?(&|$)", "i");

var local_ingred_upload_set = new Set();

function htmlToElement(html) {
    var template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.firstChild;
}

function createHTML(ingred) {
    return htmlToElement('<li class="list-group-item">' + ingred + '<span class="remove"><span class="btn btn-sm btn-default" onclick=""><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></span></span></li>');
}

function extractList(res) {
    var list_val = res[0].substring(res[0].lastIndexOf('=') + 1);
    if (list_val.indexOf('&') !== -1) {
        list_val = list_val.replace('&', '');
    }
    return list_val;
}

function addToIngredListQuery(ingred) {
    var uri = window.location.href;
    var res;
    if (res = uri.match(ingredRegex)) {
        var list_val = extractList(res);
        if (list_val.length == 0) {
            list_val = ingred;
        } else {
            list_val = list_val + ',' + ingred;
        }
        return uri.replace(ingredRegex, '$1' + 'ingred_list' + "=" + list_val + '$2');
    }
    else {
        var separator = uri.indexOf('?') !== -1 ? "&" : "?";
        return uri + separator + 'ingred_list' + "=" + ingred;
    }
}

function addToExcludeListQuery(exclude) {
    var uri = window.location.href;
    var res;
    if (res = uri.match(excludeRegex)) {
        var list_val = extractList(res);
        if (list_val.length == 0) {
            list_val = exclude;
        } else {
            list_val = list_val + ',' + exclude;
        }
        return uri.replace(excludeRegex, '$1' + 'exclude_list' + "=" + list_val + '$2');
    }
    else {
        var separator = uri.indexOf('?') !== -1 ? "&" : "?";
        return uri + separator + 'exclude_list' + "=" + exclude;
    }
}

function removeIngred(ingred) {
    var uri = window.location.href;
    var re = new RegExp('(,?)' + ingred + '(,?)', "i");
    var res;
    if (res = uri.match(re)) {
        if (res[1].length > 0) {
            return uri.replace(re, '$2');
        } else {
            return uri.replace(re, '');
        }
    } else {
        return uri;
    }
}

function updateURL(url) {
    if (history.pushState) {
        window.history.pushState({path:url}, '', url);
    } else {
        window.location.href = url;
    }
}

function loadIngredients() {
    var uri = window.location.href;
    var res;
    if (res = uri.match(ingredRegex)) {
        var list_val = res[0].substring(res[0].lastIndexOf('=') + 1);
        var tokens = list_val.split(',');
        var include_list = document.getElementById('ingred_list');
        tokens.forEach(function(e) {
            if (e.indexOf('&') !== -1) {
                e = e.replace('&', '');
            }
            if (e.length > 0 && !local_ingred_set.has(e) && !local_exclude_set.has(e)) {
                ingred_list.appendChild(createHTML(e));
                local_ingred_set.add(e);
            }
        });
    }
}

function loadExcludes() {
    var uri = window.location.href;
    var res;
    if (res = uri.match(excludeRegex)) {
        var list_val = res[0].substring(res[0].lastIndexOf('=') + 1);
        var tokens = list_val.split(',');
        var exclude_list = document.getElementById('exclude_list');
        tokens.forEach(function(e) {
            if (e.indexOf('&') !== -1) {
                e = e.replace('&', '');
            }
            if (e.length > 0 && !local_ingred_set.has(e) && !local_exclude_set.has(e)) {
                exclude_list.appendChild(createHTML(e));
                local_exclude_set.add(e);
            }
        });
    }
}

function addIngredientOnLandingPage(ingred) {
    if (ingred.length > 0 && !local_ingred_set.has(ingred) && !local_exclude_set.has(ingred)) {
        var ingred_list = document.getElementById('ingred_list');
        ingred_list.appendChild(createHTML(ingred));
        updateURL(addToIngredListQuery(ingred));
        local_ingred_set.add(ingred);
    }
}

function addExcludeOnLandingPage(exclude) {
    if (exclude.length > 0 && !local_ingred_set.has(exclude) && !local_exclude_set.has(exclude)) {
        var exclude_list = document.getElementById('exclude_list');
        exclude_list.appendChild(createHTML(exclude));
        updateURL(addToExcludeListQuery(exclude));
        local_exclude_set.add(exclude);
    }
}

$(function(){
    // Load ingredients and excludes from query string
    loadIngredients();
    loadExcludes();

    // Bind adding/removing ingredients
    $('#addIngredient').submit(function(e) {
        e.preventDefault();
        var ingred_input = $(this).find('input');
        var ingred = ingred_input.val().toLowerCase();
        ingred_input.val('');
        addIngredientOnLandingPage(ingred);
    });

    $('#addExclude').submit(function(e) {
        e.preventDefault();
        var exclude_input = $(this).find('input');
        var exclude = exclude_input.val().toLowerCase();
        exclude_input.val('');
        addExcludeOnLandingPage(exclude);
    });

    $('#ingred_list').on('click', 'span.remove', function (e) {
        var include_list = document.getElementById('ingred_list');
        var ingred = this.parentNode.textContent;
        local_ingred_set.delete(ingred);
        include_list.removeChild(this.parentNode);
        updateURL(removeIngred(ingred));
    });

    $('#exclude_list').on('click', 'span.remove', function (e) {
        var exclude_list = document.getElementById('exclude_list');
        var ingred = this.parentNode.textContent;
        local_exclude_set.delete(ingred);
        exclude_list.removeChild(this.parentNode);
        updateURL(removeIngred(ingred));
    });

    $('#submitQuery').on('click', function (e) {
        var ingred_list = Array.from(local_ingred_set);
        var exclude_list = Array.from(local_exclude_set);
        $.post('submit_query', {'ingredients[]': ingred_list, 'excludes[]': exclude_list}, function(data) {
            var results = document.getElementById('results');
            results.innerHTML = data;
        });
    });

    $('#saveQuery').on('click', function (e) {
        var ingred_list = Array.from(local_ingred_set);
        var exclude_list = Array.from(local_exclude_set);
        $.post('save_ingredients', {'ingredients[]': ingred_list, 'excludes[]': exclude_list}, function(data) {
            alert("Ingredients saved to your account!");
        });
    });

    $('#loadQuery').on('click', function (e) {
        $.post("/load_ingredients", function(data) {
            data = $.parseJSON(data);
            data.ingred_list.forEach(addIngredientOnLandingPage);
            data.exclude_list.forEach(addExcludeOnLandingPage);
        });
    });

    $('#addIngredientUpload').submit(function(e) {
        // alert("hello world");
        e.preventDefault();
        var ingred_input = $(this).find('input');
        var ingred = ingred_input.val().toLowerCase();
        ingred_input.val('');
        if (ingred.length > 0 && !local_ingred_upload_set.has(ingred)) {
            var ingred_list = document.getElementById('upload_list');
            ingred_list.appendChild(createHTML(ingred));
            local_ingred_upload_set.add(ingred);
        }
    });

    $('#upload_list').on('click', 'span.remove', function (e) {
        var upload_ingred_list = document.getElementById('upload_list');
        var ingred = this.parentNode.textContent;
        local_ingred_set.delete(ingred);
        upload_ingred_list.removeChild(this.parentNode);
    });

    $('#uploadRecipe').on('click', function(e) {
        var name_input = $(document.getElementById('recipeName')).find('input');
        var name = name_input.val();
        var link_input = $(document.getElementById('recipeLink')).find('input');
        var link = link_input.val().toLowerCase();
        var desc_input = $(document.getElementById('recipeDescription')).find('input');
        var desc = desc_input.val()
        var no_name = name.length <= 0; 
        var no_link = link.length <= 0;
        var no_desc =  desc.length <= 0;
        var no_ingred = local_ingred_upload_set.size == 0;
        var no_check = document.getElementById('check').checked == false; 

        if (no_name || no_link || no_desc || no_ingred || no_check) {
            var msg = "Please fill out missing items before submitting: \n\n";
            if (no_name) {
                msg = msg + "Missing recipe name \n";
            }
            if (no_link) {
                msg = msg + "Missing link to recipe \n";
            }
            if (no_desc) {
                msg = msg + "Missing description \n";
            }
            if (no_ingred) {
                msg = msg + "Missing ingredient list \n";
            }
            if (no_check) {
                msg = msg + "Please agree to our terms and conditions \n";
            }
            alert(msg);
        } else {
            var ingred_list = Array.from(local_ingred_upload_set);
            $.post('create', {'ingredients[]': ingred_list, 'instructions':link, 'name':name, 'description':desc}, function(data) {
                alert("Thank you for uploading!");
                window.location.replace('/');

            })
            .fail(function(data) {
                alert(data.responseText);
            });
        }
    });
});
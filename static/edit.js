var local_ingred_set = new Set();

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
    var ingred_list = document.getElementById('edit_list');
    var items = ingred_list.getElementsByTagName('li');

    for (var i = 0; i < items.length; i++) {
        var li = items[i];
        var ingred = li.firstChild.textContent;
        local_ingred_set.add(ingred);
    }
}

$(function(){
    // Load ingredients
    loadIngredients();

    $('#ingred_list').on('click', 'span.remove', function (e) {
        var include_list = document.getElementById('ingred_list');
        var ingred = this.parentNode.textContent;
        local_ingred_set.delete(ingred);
        include_list.removeChild(this.parentNode);
        updateURL(removeIngred(ingred));
    });

    $('#addIngredientEdit').submit(function(e) {
        e.preventDefault();
        var ingred_input = $(this).find('input');
        var ingred = ingred_input.val().toLowerCase();
        ingred_input.val('');
        if (ingred.length > 0 && !local_ingred_set.has(ingred)) {
            var ingred_list = document.getElementById('edit_list');
            ingred_list.appendChild(createHTML(ingred));
            local_ingred_set.add(ingred);
        }
    });

    $('#edit_list').on('click', 'span.remove', function (e) {
        var edit_ingred_list = document.getElementById('edit_list');
        var ingred = this.parentNode.textContent;
        local_ingred_set.delete(ingred);
        edit_ingred_list.removeChild(this.parentNode);
    });

    $('#editRecipe').on('click', function(e) {
        var name = $('#recipe-name').val()
        var link = $('#recipe-link').val().toLowerCase();
        var desc = $('#recipe-description').val();
        var image = $('#recipe-photo').val();
        var no_name = name.length <= 0; 
        var no_link = link.length <= 0;
        var no_desc =  desc.length <= 0;
        var no_ingred = local_ingred_set.size == 0;
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
            var form =  document.getElementById("recipeEditForm");

            var ingred_list = Array.from(local_ingred_set);
            for (var i = 0; i < ingred_list.length; i++) {
                var input = document.createElement("input");
                input.type = "hidden";
                input.name = "ingredients[]"
                input.value = ingred_list[i];
                form.appendChild(input); // put it into the DOM
            }

            var formData = new FormData(form);

            $.ajax({
                type: 'POST',
                data: formData,
                url: window.location.href,
                cache: false,
                contentType: false,
                processData: false,
                success: function(data) {
                    alert("Saved your changes!");
                    window.location.replace('/');
                },
                error: function(data) {
                    alert(data.responseText);
                }
            });
        }
    });

    $('#deleteRecipe').on('click', function(e) {
        if (confirm("Deleting objects is irreversible. Do you want to continue?")) {
            $.post("/delete/" + $("#recipe-name").val());
            window.location.replace('/');
        }
    });
});
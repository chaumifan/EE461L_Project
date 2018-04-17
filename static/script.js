function htmlToElement(html) {
    var template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.firstChild;
}

function createIngredHTML(ingred) {
    return htmlToElement('<li class="list-group-item">' + ingred + '<span class="remove"><span class="btn btn-sm btn-default" onclick=""><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></span></span></li>');
}

function updateIngredList(ingred) {
    var uri = window.location.href;
    var re = new RegExp("([?&])ingred_list=.*?(&|$)", "i");
    var separator = uri.indexOf('?') !== -1 ? "&" : "?";
    var res;
    if (res = uri.match(re)) {
        console.log(res);
        var list_val = res[0].substring(res[0].lastIndexOf('=') + 1);
        list_val = list_val + ',' + ingred;
        return uri.replace(re, '$1' + 'ingred_list' + "=" + list_val + '$2');
    }
    else {
        return uri + separator + 'ingred_list' + "=" + ingred;
    }
}

function createExcludeHTML(exclude) {
    return htmlToElement('<li class="list-group-item">' + exclude + '<span class="remove"><span class="btn btn-sm btn-default" onclick=""><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></span></span></li>');
}

function updateExcludeList(exclude) {
    var uri = window.location.href;
    var re = new RegExp("([?&])exclude_list=.*?(&|$)", "i");
    var separator = uri.indexOf('?') !== -1 ? "&" : "?";
    var res;
    if (res = uri.match(re)) {
        console.log(res);
        var list_val = res[0].substring(res[0].lastIndexOf('=') + 1);
        list_val = list_val + ',' + exclude;
        return uri.replace(re, '$1' + 'exclude_list' + "=" + list_val + '$2');
    }
    else {
        return uri + separator + 'exclude_list' + "=" + exclude;
    }
}

$(function(){
    $('#addIngredient').submit(function(e) {
        e.preventDefault();
        var ingred_input = $(this).find('input');
        var ingred = ingred_input.val().toLowerCase();
        ingred_input.val('');
        var list = document.getElementById('ingred_list');
        list.appendChild(createIngredHTML(ingred));
        if (history.pushState) {
            var newurl = updateIngredList(ingred);
            window.history.pushState({path:newurl},'',newurl);
        }
    });

    $('#addExclude').submit(function(e) {
        e.preventDefault();
        var exclude_input = $(this).find('input');
        var exclude = exclude_input.val().toLowerCase();
        exclude_input.val('');
        var list = document.getElementById('exclude_list');
        list.appendChild(createIngredHTML(exclude));
        if (history.pushState) {
            var newurl = updateExcludeList(exclude);
            window.history.pushState({path:newurl},'',newurl);
        }
    });
});
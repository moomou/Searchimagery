function getWebSiteName(input) {
    parts = input.split(".")
    if (parts.length == 3) {
        return parts[1];
    }
    return parts[0];
}

function dispWebSearchResult(queryResult) {
    var ul = $('<ul />', {
        'class' : 'siteList'
    });

    var sites = Object.keys(queryResult);

    for (var i = 0; i < sites.length; i++) {
        var li  = $('<li />',{
        });

        var detailedInfo = queryResult[i][1]
        var siteName = queryResult[i][0]

        var siteURL = detailedInfo['favicon']; 
        var count = detailedInfo['count'];

        for (var j = 0; j < COMMON_WEB.length; j++) {
            if (siteURL.match(COMMON_WEB[j]['site'])) {
                sendCmd(COMMON_WEB[j]['func']+" "+siteName);
                break;
            }
        }

        li.html(
            '<img style="max-width:10%" src="http://g.etfv.co/http://'+siteURL+'"></img>'+ " x " + count + 
            '<br />' +
            '<p class="URL">'+siteName+"</p>"
        );
        
        ul.append(li);
    }

    $('#infoBox').html("");
    $('#infoBox').append(ul);
}

function dispVideoSearchResult(queryResult) {
}

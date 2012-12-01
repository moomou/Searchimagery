/*
 For Youtube Searches
*/
var globalQueryResults;
var VIDEOURL = "https://gdata.youtube.com/feeds/api/videos/" 
var $domElement;
var playerWidth = 300;
var playerHeight = 300;

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        console.log('loading...');

        videoUrl = ytplayer.getVideoUrl();  
        console.log(videoUrl);
        var videoId = videoUrl.match(/v=.*&/)[0]; 
        videoId = videoId.substring(2,videoId.length-1);
        console.log(videoId);

        var queryUrl = VIDEOURL+videoId+'?v=2'; 
        xmlhttp = new XMLHttpRequest();
        xmlhttp.open('GET', queryUrl, false); 
        xmlhttp.send();

        xmlDoc = xmlhttp.responseXML;
        console.log(xmlDoc);
        $xmlDoc = $(xmlDoc);
        songTitle = $($xmlDoc.find('title')[0]).text(); 
        rating = $($xmlDoc.find('rating')[0]).attr('average');

        console.log(songTitle);
        console.log(rating);
   
        //special parsing of title...
        //skip if ratings too low 
        SearchEngine.sendQuery(songTitle.split(" ")[0]+
                    songTitle.split(" ")[1] + ' wiki'); 
        SearchEngine.sendQuery(songTitle.split(" ")[0]+
                    songTitle.split(" ")[1]+ ' j-lyric'); 
    }
}

function onPlayerReady(event) {
    console.log("YtPlayer ready!");
    startYoutubePlay();
}

function startYoutubePlay() {
    //start 2 to remove PL - fuck GOOGLE!
    ytplayer.cuePlaylist(globalQueryResults[1]['id'].substr(2));
    ytplayer.playVideo();
}

function stopVideo() {
    ytplayer.stopVideo();
}

function initPlayer(playlist, ele) {
    var tag = document.createElement('script');
    tag.src = "//www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    
    $domElement = ele;
    globalQueryResults = playlist;

    playerHeight = $domElement.height();
    playerWidth = $domElement.width();
}

function onYouTubeIframeAPIReady() {
    ytplayer = new YT.Player('ytPlayer', {
        height: playerHeight,
        width: playerWidth,
        control: 0,
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });

    $(window).resize(function() {
        playerHeight = $domElement.height();
        playerWidth = $domElement.width();
        ytplayer.setSize( playerHeight, playerWidth);
    });
}

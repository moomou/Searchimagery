var SearchEngine = (function() {
	//private
	var channel = undefined;
	var socket = undefined;
	var connected = false;
	var channelToken = '';
	var channelName = '';
	var searchQueue = new Array();

	var onMessage = function(res) {
		data = JSON.parse(res.data);
		
        if (data.cardType == 'yPlaylist') {
            if ($('#player').length == 0) {
            	var target = App.NextCol().add({'cardId':'player',
            									'cardType': 'card-media',
            									'cardContent': '<div id="ytPlayer"></div>'});
            	console.log(data.cardContent);
                initPlayer(data.cardContent, $('#player').parent());
            }
            else { //already loaded
                //loadYtSearchResult(data);
                //startYoutubePlay();
            }
        }
        else { //generic data
        	console.log(data.cardId);
        	var card = $('#'+data.cardId);
        	var target;
        	
        	if (card.length) {
        		target = card;
        	}
        	else {
        		target = App.NextCol().add(data);
        	}
        }
	};
	var onOpened = function() {
		connected = true;
	};
	var onError = function() {

	};
	var onClose = function() {

	};

	var sendMessage = function(path, query) {
		path += '?q=' + query[0];
		path += '&cmd= ' + query[1] || "";
		path += '&channelName=' + channelName;
		console.log('---New Query---');
		console.log(path);
  	    var xhr = new XMLHttpRequest();
	  	xhr.open('GET', path, true);
	  	xhr.send();
	};

	var createChannel = function(channelData) {
		channelName = channelData['channelName'];
		channelToken = channelData['channelToken'];

		channel = new goog.appengine.Channel(channelToken);
		socket = channel.open();

		socket.onopen = onOpened;
    	socket.onmessage = onMessage;
    	socket.onerror = onError;
    	socket.onclose = onClose;

    	console.log('createChannel finished');
	};

	var establishChannel = function() {
		var uniqueId = Math.random().toString().replace('.','');
	    var request = $.ajax({
	            url:'/query/',
	            type:'POST',
	            data: {'id':uniqueId},
	            dataType: 'json'
	        })
	        .done(function(data) {
	 			console.log(data);
	 			createChannel(data);

				while (searchQueue.length > 0) {
					sendMessage('/query/',searchQueue.pop());	
				}
	        })
	        .fail(function(data) {
	        })
	        .always(function(data) {
	        });
	};

	return {
		//public
		sendQuery : function(searchTerm, searchType) {
			
			if (searchTerm != "") {
				searchQueue.push([searchTerm, searchType]);
	    	}

			if (!channelToken) {
				establishChannel();
			}
			else {
				while (searchQueue.length > 0) {
					sendMessage('/query/',searchQueue.pop());	
				}
			}
		},
		closeSocket : function(input) {

		}
	};
})();
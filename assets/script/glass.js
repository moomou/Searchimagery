/*
 Generic Javascript library for creating Glass 
 And its support functions
*/

Array.prototype.shuffle = function() {
    var ret = this.slice()
 	var len = this.length;

	var i = len;
	while (i--) {
	    var p = parseInt(Math.random()*len);
		var t = ret[i];
    	ret[i] = ret[p];
     	ret[p] = t;
 	}
    
    return ret;
};

String.prototype.hashCode = function(){
	var hash = 0;
	if (this.length == 0) return hash;
	for (i = 0; i < this.length; i++) {
		char = this.charCodeAt(i);
		hash = ((hash<<5)-hash)+char;
		hash = hash & hash; // Convert to 32bit integer
	}
	return hash;
}

function Option (iconNames) {
    this.$ = $('<div />', {
        'class': 'Options'
    });

    for (var i in iconNames) {
        this.$.append($('<i />', {
            'class': 'icon-'+iconNames[i],
            'style': 'margin-left:5px'
        }));
    }
}

var sizes = new Array(2,4,6,8)

Glass.prototype.glassInitColor = function() {
        var randomColor = Math.floor(Math.random()*16777215).toString(16)
        return randomColor; 
    };

function Glass (id, content, options) {
    this.size = options['size'] || 2;
    this.color = options['color'] || this.glassInitColor();
    this.showMenu = options['menu'] || true;
    this.video = options['video'] || false; 
    
    var glassContentVideoStyle = this.video ? 'overflow: hidden' : '';

    this.$= $('<div />', {
        'class': "span"+this.size+" Glass",
        'id': id,
        'style': 'background: #'+this.color 
    });
    
    var glassContent = $('<div />', {
        'class': 'GlassContent',
        'style': glassContentVideoStyle
    });

    var glassContentContainer = $('<div />', {
        'class': 'GlassContentContainer',
        'html': content
    });

    glassContent.append(glassContentContainer);

    this.glassContentContainer = glassContentContainer
    this.$.append(glassContent);
    this.$.append(new Option(new Array("thumbs-up",
                                        "thumbs-down",
                                        "th-large",
                                        "th",
                                        "th-list",
                                        "headphones"
                                       )).$);
}

Row.prototype.getGlassStyles = function(style) {
    if (!style) {
        style =(Math.round((Math.random())*100))%6+1;
    }
    switch (style) {
        case 1: 
            return new Array(2,4,4).shuffle(); 
        case 2:
            return new Array(2,2,2,2,2).shuffle();
        case 3:
            return new Array(2,6,2).shuffle();    
        case 4:
            return new Array(8,2).shuffle();    
        case 5:
            return new Array(2,2,2,4).shuffle();    
        case 6:
            return new Array(6,4).shuffle();    
    }
}

Row.prototype.fillRow = function(content,start) {
    var glassStyles = this.getGlassStyles();

    for (var j = 0; j < glassStyles.length; j++) {
        if (start == content.length)
            break;

        var newGlass = new Glass(String.hashCode(),"", {'size': glassStyles[j]});
        this.$.append(newGlass.$);
        start++
    }

    return start;
}

//can only add up to 10
Row.prototype.addBox = function(id, content, options) {
    if (this.remainingSpace < options['size']) {
        size = this.remainingSpace;
    }
    
    var newGlass = new Glass(id, content, options); 
    this.$.append(newGlass.$); 
    console.log(newGlass.glassContentContainer.children().width()); 
    if (newGlass.glassContentContainer.children().width() > newGlass.$.width()*1.05) {
        newGlass.$.attr('class','span'+(options['size']+1)+" Glass");
    }


    this.remainingSpace -= options['size'];
}

function Row (canvasDOM) {
    this.remainSpace = 10;
    
    this.$= $('<div />', {
        'class': 'row-fluid', 
    });
    
    canvasDOM.append(this.$);
}



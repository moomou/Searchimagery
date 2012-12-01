//'<!--Start of Build In Javascript Template-->'
var Template = (function() {
  var cardTemplate = 
      '<div id="<%=cardId%>" class="card-header">' +
        '<legend contenteditable="<%=editable%>" class="card-title">' +
        	'<%=cardTitle%>' +
        '</legend>' +
        '<div class="pull-right" style="margin-top:-3.7em; padding-right: 0.5em;">' +
          '<ul class="nav rating">' +
            '<li style="opacity:0.5;"><i class="icon-heart"></i></li>' + 
            '<li style="opacity:0.5;"><i class="icon-heart"></i></li>' +
            '<li style="opacity:0.5;"><i class="icon-heart"></i></li>' +
            '<li style="opacity:0.5;"><i class="icon-heart"></i></li>' +
            '<li style="opacity:0.5;"><i class="icon-heart"></i></li>' +
          '</ul>' +
        '</div>' +
      '</div>' +
      '<div class="contentContainer outer">' +
        '<div contenteditable="<%=editable%>" class="inner card-content">' + 
          '<%=cardContent%>' +
        '</div>' + 
      '</div>' +
     	'<div class="actions outer">' +
     	  '<div class="inner">' +
     	    '<button data-src="<%=cardSrc%>" class="btn"><i class="icon-share"></i> Share</button>' +
          '&nbsp;' +
     	    '<button data-src="<%=cardSrc%>" class="btn"><i class="icon-globe"></i> Visit</button>' +
     	  '</div>' +
      '</div>';
  
  return {
    cardTemplate: cardTemplate
  };
}) ();
    
      
    

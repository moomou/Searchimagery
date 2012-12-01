//Global Vars
var queryTypes = {"g":"/web","y":"/video"};

function keyShortcut() {
    $(document).keydown(function(e){
        if (e.keyCode == 191) { //back slash 
            if (e.ctrlKey) {
                $('#searchbar').focus();
            }
            else {
                $('#cmdLine').focus();
            } 
            return false;
        }
    });
}

function visitBtn() {

}

function shareBtn() {

}

function addBtn() {
var target = App.NextCol().add({'editable': true});
}

function downloadBtn() {

}

$(function() {
    $('#addBtn').click(addBtn);
    $('#downloadBtn').click(downloadBtn);
    
    $('.icon-search').click(function() {
        $('#searchForm').submit();
    });
    
    //settings
    $('#searchForm').submit(function() {
        var input = $('#searchbar').val();
        SearchEngine.sendQuery(input);
        return false;
    });

    keyShortcut();
});

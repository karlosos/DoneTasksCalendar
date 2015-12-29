//var name = "dodawanie";
//var page = require('webpage').create();
//var url = 'html/_'+name+'.html';
//var output = 'html/_'+name+'.png';
//
//page.open(url, function (status) {
//if (status !== 'success') {
//    console.log('Unable to load the address!');
//    phantom.exit();
//} else {
//    window.setTimeout(function () {
//        page.render(output);
//        phantom.exit();
//    }, 1000); // Change timeout as required to allow sufficient time
//}
//});
//

var page = require('webpage').create(), loadInProgress = false, fs = require('fs');
var htmlFiles = new Array();

var curdir = phantom.args[0] || fs.workingDirectory;
var curdirList = fs.list(curdir);
console.log("dir file count: " + curdirList.length);

for(var i = 0; i< curdirList.length; i++) {
    var fullpath = curdir + fs.separator + curdirList[i];
    if(fs.isFile(fullpath)) {
        if(fullpath.toLowerCase().indexOf('.html') != -1) {
            htmlFiles.push(fullpath); // todo: make this more async (i.e. pop on/off stack WHILE rending pages)
        }
    }
}

//console.log('HTML files found: ' + htmlFiles.length);

var pageindex = 0;
var fileName = '';

var interval = setInterval(function() {
    if (!loadInProgress && pageindex < htmlFiles.length) {
        fileName = htmlFiles[pageindex];
        page.open(htmlFiles[pageindex]);
    }
    if (pageindex == htmlFiles.length) {
        console.log("<< Image render complete! >>");
        phantom.exit();
    }
}, 1200);

page.onLoadStarted = function() {
    loadInProgress = true;
};

page.onLoadFinished = function() {
    loadInProgress = false;
    var dest = "html/images/" + fileName.substr(6, fileName.length) + ".png";
    console.log('saving: ' + dest);

    page.evaluate(
      function () {
        var scaleVal = "scale("+arguments[0] || '1.0'+")";
        document.body.style.webkitTransform = scaleVal;
      },
      phantom.args[1]
    );

    console.log("1 sec");
    setTimeout(function () {
        console.log("3 sec");
        page.render(dest);
    }, 1000); // Change timeout as required to allow sufficient time


    pageindex++;
}

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

/* tested on PhantomJS 1.6 */

var page = require('webpage').create(), loadInProgress = false, fs = require('fs');
var htmlFiles = new Array();

// console.log(fs.workingDirectory);
// console.log(phantom.args[0]);

var curdir = phantom.args[0] || fs.workingDirectory;
var curdirList = fs.list(curdir);
console.log("dir file count: " + curdirList.length);

// loop through files and folders //
for(var i = 0; i< curdirList.length; i++) {
    var fullpath = curdir + fs.separator + curdirList[i];
    // check if item is a file //
    if(fs.isFile(fullpath)) {
        // check that file is html //
        if(fullpath.toLowerCase().indexOf('.html') != -1) {
            // show full path of file //
            // console.log('File path: ' + fullpath);
            htmlFiles.push(fullpath); // todo: make this more async (i.e. pop on/off stack WHILE rending pages)
        }
    }
}

console.log('HTML files found: ' + htmlFiles.length);

// output pages as PNG //
var pageindex = 0;
var fileName = '';

var interval = setInterval(function() {
    if (!loadInProgress && pageindex < htmlFiles.length) {
        // console.log("image " + (pageindex + 1) + " of " htmlFiles.length);
        fileName = htmlFiles[pageindex];
        page.open(htmlFiles[pageindex]);
    }
    if (pageindex == htmlFiles.length) {
        console.log("<< Image render complete! >>");
        phantom.exit();
    }
}, 1000);

page.onLoadStarted = function() {
    loadInProgress = true;
    // console.log('page ' + (pageindex + 1) + ' load started');
};

page.onLoadFinished = function() {
    loadInProgress = false;
    var dest = "images/" + fileName + ".png";
    console.log('saving: ' + fileName + ".png");

    page.evaluate(
      function () {
        var scaleVal = "scale("+arguments[0] || '1.0'+")";
        document.body.style.webkitTransform = scaleVal;
      },
      phantom.args[1]
    );

    page.render(dest); // RENDER PAGE //

//    window.setTimeout(function () {
//        page.render(dest);
//    }, 1000); // Change timeout as required to allow sufficient time


    // console.log('page ' + (pageindex + 1) + ' load finished');
    pageindex++;
}
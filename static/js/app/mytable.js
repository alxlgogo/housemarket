var theTable = document.getElementById("tablePage");
var spanPre = document.getElementById("spanPre");
var spanNext = document.getElementById("spanNext");
var pageList = document.getElementById("pageList");
var spanPageN = pageList.getElementsByTagName("li");

var numberRowsInTable = theTable.rows.length;
var pageSize = 10;
var pageSize = 7;
var page = 1;


function clearActive() {
    for (var i = 1; i < spanPageN.length - 1; i++) {
        console.log(spanPageN[i].id);
        spanPageN[i].setAttribute("class", "");
    }
}

//next page
function next() {
    hideTable();
    //the last column of this page
    currentRow = pageSize * page;
    maxRow = currentRow + pageSize;

    if (maxRow > numberRowsInTable) {
        maxRow = numberRowsInTable;
    }
    for (var i = currentRow; i < maxRow; i++) {
        theTable.rows[i].style.display = '';
    }
    page++;
    if (maxRow == numberRowsInTable) {
        console.log(maxRow + "=======");
        nextOff();
    }
    preOn();
    showPageActive(page);
}

//previous page
function pre() {

    hideTable();
    page--;

    currentRow = pageSize * page;
    maxRow = currentRow - pageSize;
    if (currentRow > numberRowsInTable) currentRow = numberRowsInTable;
    for (var i = maxRow; i < currentRow; i++) {
        theTable.rows[i].style.display = '';
    }

    if (maxRow == 0) {
        preOff();

    }
    showPageActive(page);
    nextOn();

}

//page number
function nPage(n) {
    hideTable();

    currentRow = pageSize * (n - 1);
    maxRow = currentRow + pageSize;
    if (currentRow > numberRowsInTable) currentRow = numberRowsInTable;
    for (var i = currentRow; i < maxRow; i++) {
        theTable.rows[i].style.display = '';
    }


    if (n == 1) {
        preOff();
    } else if (n * pageSize == numberRowsInTable) {
        nextOff();
    } else {
        nextOn();
        preOn();
    }
    showPageActive(n);

}

function hideTable() {
    for (var i = 0; i < numberRowsInTable; i++) {
        theTable.rows[i].style.display = 'none';
    }
}

//set current page as active
function showPageActive(p) {
    clearActive();
    var nowpage = document.getElementById('spanpage' + p);
    console.log(nowpage.id);
    nowpage.setAttribute("class", "active");

}

//total page
function pageCount() {
    var count = 0;
    if (numberRowsInTable % pageSize != 0) count = 1;
    return parseInt(numberRowsInTable / pageSize) + count;
}


function preOn() {
    spanPre.innerHTML = " <a href='javascript:pre();'>&laquo;</a>";
    spanPre.setAttribute("class", "");
}

function preOff() {
    spanPre.innerHTML = " <a href='javascript:void(0);'>&laquo;</a>";
    spanPre.className = "disabled";
}

function nextOn() {
    spanNext.innerHTML = "<a href='javascript:next()'>&raquo;</a>";
    spanNext.setAttribute("class", "");
}

function nextOff() {
    spanNext.innerHTML = "<a href='javascript:void(0)'>&raquo;</a>";
    spanNext.setAttribute("class", "disabled");
}


function hide() {
    for (var i = pageSize; i < numberRowsInTable; i++) {
        theTable.rows[i].style.display = 'none';
    }
    preOff();
    nextOn();
}

hide();

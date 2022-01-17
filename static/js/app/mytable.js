var theTable = document.getElementById("tablePage");
var spanPre = document.getElementById("spanPre");
var spanNext = document.getElementById("spanNext");
var pageList = document.getElementById("pageList");
var spanPageN = pageList.getElementsByTagName("li");

var numberRowsInTable = theTable.rows.length;
// var pageSize = 10;
var pageSize = 7;
var page = 1;

//清除列表的active样式
function clearActive() {
    for (var i = 1; i < spanPageN.length - 1; i++) {
        console.log(spanPageN[i].id);
        spanPageN[i].setAttribute("class", "");
    }
}

//下一页
function next() {
    hideTable();
    //当前最后一行行数
    currentRow = pageSize * page;
    maxRow = currentRow + pageSize;
    // 判断是否到了table最后几行数据
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

//上一页
function pre() {

    hideTable();
    page--;

    currentRow = pageSize * page;
    maxRow = currentRow - pageSize;
    if (currentRow > numberRowsInTable) currentRow = numberRowsInTable;
    for (var i = maxRow; i < currentRow; i++) {
        //清除display样式，display将使用默认
        theTable.rows[i].style.display = '';
    }

    if (maxRow == 0) {
        preOff();

    }
    showPageActive(page);
    nextOn();

}

//第几页
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

//将当前页设为active
function showPageActive(p) {
    //清除之前的
    clearActive();
    var nowpage = document.getElementById('spanpage' + p);
    console.log(nowpage.id);
    nowpage.setAttribute("class", "active");

}

//总共页数
function pageCount() {
    var count = 0;
    //判断是否整除
    if (numberRowsInTable % pageSize != 0) count = 1;
    return parseInt(numberRowsInTable / pageSize) + count;
}


//上一页下一页链接的禁用和打开
function preOn() {
    spanPre.innerHTML = " <a href='javascript:pre();'>&laquo;</a>";
    spanPre.setAttribute("class", "");
}

function preOff() {
    //bootstrap设置禁用样式之后还是可以点击一次，所以这里直接修改innerHTML解决这个问题。
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


//隐藏表格 ,只显示第一页的内容
function hide() {
    for (var i = pageSize; i < numberRowsInTable; i++) {
        theTable.rows[i].style.display = 'none';
    }
    preOff();
    nextOn();
}

hide();

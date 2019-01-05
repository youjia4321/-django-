window.onload = function(){
    autoMove('li', 'span');
};

function autoMove(tagImg, tagSpan){
    var imgs = document.getElementsByTagName(tagImg);
    var spans = document.getElementsByTagName(tagSpan);
    function InitMove(index){
        for(var i = 0; i < imgs.length; i++){
            imgs[i].style.display = "none";
            spans[i].style.background = "white";
        }
        imgs[index].style.display = "block";
        spans[index].style.background = "red";
    }
    InitMove(0);
    var speed = 3000;
    var count = 1;
    function fMove(){
        if (count == imgs.length){
            count = 0;
        }
        InitMove(count);
        count++;
    }
    var myBar = setInterval(fMove, speed);
    var btnleft = document.getElementById('btnleft');
    var btnright = document.getElementById('btnright');
    var hit = document.getElementById('b');
    // 鼠标停在图片上停止滑动，移除鼠标继续滑动
    hit.onmouseover = function(){
        clearInterval(myBar);
    }
    hit.onmouseout = function(){
        setInterval(fMove, speed);
    }
    // 上一张，下一张
    btnleft.onclick = function(){
         clearInterval(myBar);
         if (count == 1){
             count = imgs.length;
         }
         count--;
         myBar = setInterval(InitMove(count-1), speed);
    };
    btnright.onclick = function(){
        clearInterval(myBar);
        fMove();
        myBar = setInterval(InitMove(count-1), speed);
    };
}
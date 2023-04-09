//获取网页加载时间
var startCountdownTime = new Date().getTime();

//每 1 秒更新一次倒计时
var x = setInterval(function() {

//获取时间
  var now = new Date().getTime();
    
//获得5分钟倒计时时间
  var reminderMinutes = 5;
  var countDownTime = new Date(startCountdownTime + (reminderMinutes*60*1000));

  //计算现在和倒计时日期之间的距离
  var distance = countDownTime - now;

  //分秒的时间计算
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

//在 id="timer" 的元素中显示结果
  document.getElementById("timer").innerHTML = minutes + "m " + seconds + "s ";

//如果倒计时结束，发送提醒
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("timer").innerHTML = "时间过期";
    window.alert("请更新等待时间!");

  }
}, 1000);




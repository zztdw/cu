//获取网页加载时间
// 获取当前时间戳，单位是毫秒，用于后续计算倒计时的时间差
var startCountdownTime = new Date().getTime();

//每 1 秒更新一次倒计时
// 通过 setInterval() 方法每隔 1 秒执行一次函数，实现每秒更新倒计时的效果
var x = setInterval(function() {

//获取时间
// 获取当前时间戳，用于计算倒计时的时间差
var now = new Date().getTime();

//获得5分钟倒计时时间
// 通过设置 reminderMinutes 的值为 5，即设置倒计时时间为 5 分钟
var reminderMinutes = 5;
var countDownTime = new Date(startCountdownTime + (reminderMinutes601000));

//计算现在和倒计时日期之间的距离
// 计算当前时间和倒计时时间之间的时间差，用于显示剩余时间
var distance = countDownTime - now;

//分秒的时间计算
// 将时间差转换为分钟和秒钟的形式，用于在网页上显示剩余时间
var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
var seconds = Math.floor((distance % (1000 * 60)) / 1000);

//在 id="timer" 的元素中显示结果
// 通过 document.getElementById() 方法获取 id 为 "timer" 的元素，并将剩余时间的分钟和秒钟显示在元素中
document.getElementById("timer").innerHTML = minutes + "m " + seconds + "s ";

//如果倒计时结束，发送提醒
// 如果倒计时时间结束，即 distance < 0，则清除 setInterval() 方法的执行，并在网页上显示 "EXPIRED" 和弹出一个窗口提醒用户更新时间
if (distance < 0) {
clearInterval(x);
document.getElementById("timer").innerHTML = "EXPIRED";
window.alert("Please update time!");
}
}, 1000);
// 通过设置 setInterval() 方法的执行时间为 1000 毫秒，即每隔 1 秒执行一次该函数，实现每秒更新倒计时的效果


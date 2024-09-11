var a;
a = 'hello world';
var container = {
    caoyao:"草药",
    henau:"河南农业大学"
}
container.zhengzhou = "郑州";
console.log(container["caoyao"]);

var i = 0;
while(i<10){
    // console.log('hello');
    i++;
}
var fun = function (){
    console.log('hello');
}
console.log(typeof fun);
console.log(typeof a);

//对象
var Student = {
    name : "wjh",
    age:22,
    eat:function (){
        console.log('eat');
    }
}
for(var p in Student){
    console.log(p + '=' + Student[p]);
}
var x = 1;
var sum = (b = x++ + --x) + x-- + b ++;
console.log(sum);

var arr = ["1","2","3","4","5","6","7","8","9"];
console.log(arr.length);
var arr2 = new Array(9);
console.log(arr2.length);
console.log(arr2);
arr2.push("hello world");
arr2[0] = "hv";
console.log(arr2);
arr2.pop();
console.log(arr2);
arr.splice(2,3);
console.log(arr);
arr.splice(3,1,20,21);
console.log(arr);
var str = arr.join(',');
console.log(str);

function test(){
    // alert("调用");//浏览器弹窗
    
}
test();

function add(a,b,c){
    console.log(arguments);
    var sum = a + b + c;
    console.log(sum);
}
add(1,2,3,4);

function Fruit(name,smell,color){
    this.name=name;
    this.smell=smell;
    this.color=color;
}
var Apple = new Fruit('apple','sweet','red');
console.log(Apple);
//回调函数
function eat(food,callback){
    callback(food);
}
eat('apple',function (food){
    console.log('eat'+food);
});
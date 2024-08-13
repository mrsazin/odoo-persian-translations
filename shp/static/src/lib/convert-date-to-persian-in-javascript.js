// METHOD 1

const today = Date.now();
 
const todayFa = {
    "day" : getDateFormat(today , {"day" : "2-digit"}),
    "month" : getDateFormat(today , {"month" : "numeric"}),
    "monthTitle" : getDateFormat(today , {"month" : "long"}),
    "year" : getDateFormat(today , {"year" : "numeric"}),
    "dayWeek" : getDateFormat(today , {"weekday" : "long"}),
}
 
function getDateFormat(uDate,option){
    let date = new Intl.DateTimeFormat('fa-IR', option).format(uDate);
    return date;
} 
 
console.log(todayFa);
 
/*
{
  day: "۰۱",
  dayWeek: "جمعه",
  month: "۱۱",
  monthTitle: "بهمن",
  year: "۱۴۰۰"
}
*/

// METHOD 2
// first add farvardin.js library from https://github.com/senior-x-79/farvardin.js/tree/master/dist
// ### <script src="static/js/lib/farvardin.min.js"></script>

// from persian to normal date
console.log(farvardin.solarToGregorian(1399 , 1 , 25));  // [2020 , 4 , 13]
console.log(farvardin.solarToGregorian(1399 , 1 , 25 , "array")); // همان خروجی بالا

// from normal date to persian
console.log(farvardin.gregorianToSolar(2020 , 4 , 13 , "string")); // 1399-01-25
console.log(farvardin.gregorianToSolar(2020 , 4 , 13 , "object")); // { year: 1399, month: 1, day: 25 }
console.log(farvardin.gregorianToSolar(2020 , 4 , 13 , "json")); // {"year":1399,"month":1,"day":25}

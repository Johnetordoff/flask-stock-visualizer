

function loadGraphs(data){

      var cityGraph = data[0];
      data.shift();

      data = fixdates(data);
      oneDay = 24*60*60*1000;
      var diffDays = (data[0]['perf_dt'].getTime() - new Date().getTime())/(oneDay);
      if(diffDays>0){
        data['daysuntil'] = Math.abs(Math.round(diffDays)) + " days until showtime."
       } else{
        var str = data[0]['perf_dt'] +""
        data['daysuntil'] = "Performed on " + str.substring(0, str.length - 23);
       }
       document.getElementById("daysUntil").innerHTML = data['daysuntil'];

//      data = selectPro(name,data);
      var POS = CountPOS(data);

      var pie = c3.generate({
          bindto: '#pie',
          data: {
              columns: [
                  ['Box Office', POS["BoxOffice"]],
                  ['Web', POS["Web"]],
                  ['Sub Services', POS["SubServices"]],
                  ['Call Center', POS["CallCenter"]],
                  ['Group Sales', POS["GroupSales"]],
              ],
              type : 'pie'
          }

      });
      var days = waitdays(data);
      var daysleft = Object.keys(days).sort();
      var sales = [];
      for(var i = 0;i<daysleft.length;i++){
        sales.push(days[daysleft[i]]);
      };
      daysleft[0] = 'x1'
      sales[0] = 'Ticket Sales'

      var chart = c3.generate({
        bindto: '#chart',
        data: {
            xs: {
                'Ticket Sales': 'x1',
            },
            columns: [
                daysleft,
                sales
            ]
        },
        axis: {
            x: {
                label: 'Days Until Preformance'
            },
//            y: {
  //              show: true,
    //            label: 'Ticket Sales'
      //      },
            y2: {
                show: false,
                label: 'Purchases'
            },
        color: '#FFFFFF'

        },
        color: {
        pattern: ['#FFFFFF']
    },
    tooltip: {
     format: {
        title: function (x) { return 'Days until Preformance: ' + x; }
        },
      value: function (value, ratio, id) {
                return format("Purchases " + value);
            }
    }

    });
    var cities = [];
    var tickets = [];
    for(var i = 0; i < cityGraph.length; i++){
        cities.push(cityGraph[i]['city']);
        tickets.push(cityGraph[i]['pur']);
    }

    var noPhilCities = cities;
    var noPhilTicks = tickets;
    var PhilTicks = tickets[0];
    document.getElementById("Phillybtn").innerHTML = "Excluding  the " + PhilTicks + " tickets purchased in Philadelphia";

    noPhilCities[0] = 'x';
    noPhilTicks[0] = 'purchases';
    var colorScale = d3.scale.category10();
    var bar = c3.generate({
    bindto: "#bar",
    data: {
        x : 'x',
        columns: [
            noPhilCities.slice(0,11),
            noPhilTicks.slice(0,11),
        ],
        type: 'bar',
    labels: false,

    color: function(inColor, data) {
      if(data.index !== undefined) {
        return colorScale(data.index);
      }

      return inColor;
    },    },

    axis: {
        x: {
            type: 'category' // this needed to load string x value
        }
    }
    });

};


function CountPOS(data) {
  var Web = 0;
  var CallCenter = 0;
  var SubServices = 0;
  var BoxOffice = 0;
  var GroupSales = 0;
  for(var i=0; i<data.length; i++)
  {
    Web = data[i]["mos_desc"] == "TP Web" ? Web + 1 : Web;
    CallCenter = data[i]["mos_desc"] == "TP Call Center" ? CallCenter + 1 : CallCenter;
    BoxOffice = data[i]["mos_desc"] == "TP Box Office" ? BoxOffice + 1 : BoxOffice;
    SubServices = data[i]["mos_desc"] == "TP Sub Services" ? SubServices + 1 : SubServices;
    GroupSales = data[i]["mos_desc"] == "TP Group Sales" ? GroupSales + 1 : GroupSales;
  }
  return {'Web':Web,'CallCenter':CallCenter,'SubServices':SubServices,'BoxOffice':BoxOffice,"GroupSales":GroupSales};

};

function selectPro(pro,data) {
  newData = [];
  for(var i=0; i<data.length; i++)
  {
    if(data[i]["perf_desc"] == pro){
      newData.push(data[i]);
    }
  }
  return newData;

};

function fixdates(data) {
  for(var i=0; i<data.length; i++){
    var orderDate = data[i]['order_dt'].split(' ')[0].split('/');
    var perfDate = data[i]['perf_dt'].split(' ')[0].split('/');

    if(orderDate[2] < 1000){
      orderDate[2] = 2000 + parseInt(orderDate[2])
    }
    if(perfDate[2] < 1000){
      perfDate[2] = 2000 + parseInt(perfDate[2]);
    }

    data[i]['order_dt'] = new Date(orderDate[2],orderDate[0],orderDate[1]);
    data[i]['perf_dt'] = new Date(perfDate[2],perfDate[0],perfDate[1]);

    oneDay = 24*60*60*1000;
    var diffDays = Math.round(Math.abs((data[i]['perf_dt'].getTime() - data[i]['order_dt'].getTime())/(oneDay)))
    if(diffDays<365){
      data[i]['waitTime'] = diffDays;
    }

  }
  return data;
};


function waitdays(data) {
  waits = [];
  for(var i=0; i<data.length; i++){
     waits.push(data[i]['waitTime'])
  }
  data = foo(waits);

  return data;
};

function findAreas(data){
  places = [];
  for(var i=0; i<data.length; i++){
     if(places.indexOf(data[i]['city'])== -1){
         places.push(data[i]['city']);
     }
    }
    return places;
};

function findAllPlaces(data){
  places = [];
  for(var i=0; i<data.length; i++){

         places.push(data[i]['city']);
    }
    return places;
};

function foo(arr) {
  var obj = { };
  for (var i = 0, j = arr.length; i < j; i++) {
     obj[arr[i]] = (obj[arr[i]] || 0) + 1;
  }
  return obj
};


function change(){
    var e = document.getElementById("selectPro");
    var strUser = e.options[e.selectedIndex].value;
    document.getElementById("superTitle").innerHTML = "The Analytics of <br>" + strUser;
    $.getJSON($SCRIPT_ROOT + '/pref', {
        name: strUser,
      }, function(data) {
        var data = data['data'];
        loadGraphs(data);
    });

}

function changePro(){

    window.location = "rend";

    change();
}

$(document).ready(function(){
    change();

})

$('div.main').click(function(e)
{
    window.location = "https://www.paballet.org/upcoming-programs";
    });


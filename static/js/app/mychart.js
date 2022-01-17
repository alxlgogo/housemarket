//
// Highcharts.chart('container', {
//     title: {
//         text: 'Ireland house price, 1976-2015'
//     },
//     subtitle: {
//         text: 'Source: https://data.gov.ie/'
//     },
//     yAxis: {
//         title: {
//             text: 'Price €'
//         }
//     },
//     xAxis: {
//         accessibility: {
//             rangeDescription: 'Range: 1976 to 2015'
//         }
//     },
//     legend: {
//         layout: 'vertical',
//         align: 'right',
//         verticalAlign: 'middle'
//     },
//     plotOptions: {
//         series: {
//             label: {
//                 connectorAllowed: false
//             },
//             pointStart: 1976
//         }
//     },
//     series: [
//         { % for ser in series %
// }
// {
//     name: "{{ ser['name'] }}",
//         data
// :
//     {
//         {
//             ser['data']
//         }
//     }
// }
// ,
// {%
//     endfor %
// }
// ],
//
// responsive: {
//     rules: [{
//         condition: {
//             maxWidth: 500
//         },
//         chartOptions: {
//             legend: {
//                 layout: 'horizontal',
//                 align: 'center',
//                 verticalAlign: 'bottom'
//             }
//         }
//     }]
// }
// }
// )
// ;

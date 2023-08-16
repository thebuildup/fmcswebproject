// Wait for the DOM to load and then render the chart
document.addEventListener("DOMContentLoaded", function() {
  const seriesDataElement = document.getElementById("area-chart");
  const series = JSON.parse(seriesDataElement.getAttribute("data-series"));
  const categories = JSON.parse(seriesDataElement.getAttribute("data-categories"));
  renderChart(series, categories);
});

function renderChart(series, categories) {
    /* Get CSS Variables */
    const colorPrimary = getComputedStyle(document.documentElement)
      .getPropertyValue("--color-primary")
      .trim();

    const colorDefault = getComputedStyle(document.documentElement)
      .getPropertyValue("--color-default")
      .trim();

    const colorLabel = getComputedStyle(document.documentElement)
      .getPropertyValue("--color-label")
      .trim();

    const fontFamily = getComputedStyle(document.documentElement)
      .getPropertyValue("--font-family")
      .trim();

    /* Declare Default Chart Options */

    const defaultOptions = {
      chart: {
        toolbar: {
          show: false,
        },
        selection: {
          enabled: false,
        },
        zoom: {
          enabled: false,
        },
        width: "100%",
        height: 200,
        offsetY: 12,
      },
      dataLabels: {
        enabled: false,
      },
      legend: {
        show: false,
      },
      states: {
        hover: {
          filter: {
            type: "none",
          },
        },
      },
    };

    // Bar Chart

    var barOptions = {
      ...defaultOptions,
      chart: {
        ...defaultOptions.chart,
        type: "area",
      },
      tooltip: {
        enabled: true,
        fillSeriesColor: false,
        style: {
          fontFamily: fontFamily,
        },
        y: {
          formatter: (value) => {
            return `${value}`;
          },
        },
      },
      series: [
        {
          name: series[0].name,
          data: series[0].data,
        },
      ],
      colors: [colorPrimary],
      fill: {
        type: "gradient",
        gradient: {
          type: "vertical",
          opacityFrom: 1,
          opacityTo: 0,
          stops: [0, 100],
          colorStops: [
            [
              {
                offset: 0,
                color: "#ffffff",
                opacity: 0.2,
              },
              {
                offset: 100,
                color: "#ffffff",
                opacity: 0,
              },
            ],
          ],
        },
      },
      stroke: { colors: [colorPrimary], lineCap: "round" },
      grid: {
        borderColor: "rgba(0, 0, 0, 0)",
        padding: { left: 10, right: 0, top: -16, bottom: -8 },
      },
      markers: {
        strokeColors: colorPrimary,
      },
      yaxis: {
        show: true,
      },
      xaxis: {
        labels: {
          floating: true,
          show: true,
          style: {
            fontFamily: fontFamily,
            colors: colorLabel,
          },
        },
        axisBorder: {
          show: false,
        },
        axisTicks: {
          show: false,
        },
        crosshairs: {
          show: false,
        },
        categories: categories,
      },
    };

    var chart = new ApexCharts(document.querySelector("#area-chart"), barOptions);

    chart.render();
}
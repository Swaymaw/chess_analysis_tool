<template>
    <VChart :option="option" autoresize style="width: 100%; height: 150px" />
</template>

<script setup>
import { computed } from "vue";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart } from "echarts/charts";
import { GridComponent } from "echarts/components";
import VChart from "vue-echarts";

use([CanvasRenderer, LineChart, GridComponent]);

const props = defineProps({
    scores: { type: Array, required: true },
    moveIndex: { type: Number, required: true },
});

const option = computed(() => ({
    backgroundColor: "#222",
    xAxis: {
        type: "category",
        data: props.scores.map((_, i) => i),
        show: false,
        boundaryGap: false,
    },
    yAxis: {
        type: "value",
        show: false,
        min: 0,
        max: 20,
    },

    grid: { left: 0, right: 0, top: 0, bottom: 0 },
    progressive: 5000,
    series: [
        {
            type: "line",
            data: props.scores.map((val) => val + 10),
            smooth: true,
            showSymbol: false,
            lineStyle: { opacity: 0 },
            areaStyle: { opacity: 1.0, color: "#ddd" },
            markLine: {
                symbol: "none",
                label: { show: false },
                lineStyle: { width: 2.0, type: "solid", color: "#fff" },
                data: [{ yAxis: 10 }],
                z: 1,
            },
            z: 0,
        },
        {
            type: "line",
            data: props.scores.map(() => null), // no actual line
            showSymbol: false,
            lineStyle: { opacity: 0 },

            markLine: {
                symbol: "none",
                label: { show: false },
                lineStyle: { width: 2, type: "solid", color: "#fff" },
                data: [{ xAxis: Number(props.moveIndex) + 1 }],
                z: 1,
            },

            z: 100,
        },
    ],
}));
</script>

import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AnalysisView from "../views/AnalysisView.vue";

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/analysis", name: "analysis", component: AnalysisView, props: true },
];

export default createRouter({ history: createWebHistory(), routes });

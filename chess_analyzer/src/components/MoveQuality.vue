<template>
    <h5 class="card-title fw-bold text-muted text-uppercase small mb-0">{{ line }}</h5>
</template>
<script setup>
import { computed } from "vue";

const props = defineProps({
    move_quality: { type: String, required: true },
});

const emojiMap = {
    blunder: "💀",
    mistake: "⚠️",
    inaccuracy: "❗",
    good: "👍",
    excellent: "✨",
    best: "🏆",
    brilliant: "🌟",
};

const line = computed(() => {
    const e = emojiMap[props.move_quality.toLowerCase()] ?? "❔";
    return `This move was ${props.move_quality.toUpperCase()} ${e}.`;
});
</script>

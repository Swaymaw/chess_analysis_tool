<template>
  <div class="card border-0 shadow-sm bg-dark text-light">
    <div class="card-body p-3">
      <h6 class="small fw-bold text-uppercase opacity-50 mb-2">Engine Line</h6>

      <div v-if="isLoading" class="spinner-grow spinner-grow-sm opacity-50"></div>

      <div v-else class="engine-data font-monospace">
        <div class="d-flex justify-content-between border-bottom border-secondary pb-2 mb-2">
          <span class="text-info">Move {{ data?.move_count }}</span>
          <span>
            <span class="text-white-50">Played:</span>
            <span class="text-warning fw-bold">{{ data?.my_move }}</span>
            <span class="mx-2 text-white-50">|</span>
            <span class="text-white-50">Best:</span>
            <span class="text-success fw-bold">{{ data?.best_move }}</span>
          </span>
        </div>

        <div class="row g-0 mb-3 small">
          <div class="col-6 border-end border-secondary pe-2">
            <div class="text-white-50 x-small text-uppercase">Move Eval</div>
            <div>
              {{ data?.my_move_score > 0 ? '+' : '' }}{{ data?.my_move_score.toFixed(2) }}
            </div>
          </div>

          <div class="col-6 ps-2">
            <div class="text-white-50 x-small text-uppercase">Engine Eval</div>
            <div class="text-success">
              {{ data?.best_move_score > 0 ? '+' : '' }}{{ data?.best_move_score.toFixed(2) }}
            </div>
          </div>
        </div>

        <div class="engine-line-box">
          <h6 class="x-small fw-bold text-uppercase text-primary mb-1">Engine Continuation</h6>
          <div class="preserve-wrap bg-black bg-opacity-50 p-2 rounded small line-height-sm">
            {{ data?.engine_line?.join(' ') || 'No continuation found' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isLoading: Boolean,
  data: {
    type: Object,
    required: true
  }
})
</script>

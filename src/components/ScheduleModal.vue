<template>
<div id="schedule-modal">
  <div class="modal-mask">
    <div class="modal-wrapper">
      <div class="modal-container">
        <h3> Schedule </h3>
        <button classtype="submit" class="btn btn-danger" v-on:click="onClose">Close</button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'ScheduleModal',
  props: {
  },
  methods: {
    onClose () {
      this.$emit('onClose')
    }
  }
}
</script>

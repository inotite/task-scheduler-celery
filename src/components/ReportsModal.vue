<template>
  <div id="modal">
      <div class="modal-mask">
          <div class="modal-wrapper">
            <div class="modal-container">
               <h3> Reports </h3>
               <form>
                <div class="form-group row">
                 <label for="machine-name" class="col-sm-2 col-form-label">Machine Name: </label>
                   <div class="col-sm-10">
                     <p>{{ machineName }}</p>
                    </div>
                </div>
               <div class="form-group row">
                 <label for="machine-name" class="col-sm-2 col-form-label">Number of Tasks: </label>
                 <div class="col-sm-10">
                   <p>{{ numTasks }}</p>
                 </div>
               </div>
            </form>
            <button classtype="submit" class="btn btn-danger" v-on:click="$parent.showReportsModal = false">Close</button>
          </div>
      </div>
   </div>
</div>
</template>
<script>
export default{
  name: 'MachineInfoModal',
  props: {
    numTasks: {
      type: Number,
      required: true
    },
    machineName: {
      type: String,
      required: true
    }
  }
}
</script>
<style>
/* modal-mask handles the background  */
.modal-mask{
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  transition: opacity 0.3s ease;
}
.modal-wrapper{
    height: 100%;
}
.modal-container{
    width: 300px;
    background-color: white;
    vertical-align: middle;
    align-items: center;
    padding: 10px 10px;
    vertical-align: middle;
}
</style>

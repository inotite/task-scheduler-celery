<template>
<div>
<table>
  <reportsmodal v-if="showReportsModal" :machineName="returnMachineName" :numTasks="taskArrayLength"></reportsmodal>
  <schedulemodal v-if="showScheduleModal" :closeSchedule="closeSchedule()"></schedulemodal>
  <!--<caption @click="showModal = true" class="task-table">{{this.$parent.selectedMachine[0]['id']}}</caption>-->
<!-- check if user is authorised to delete an item -->
 <!-- <th v-if="$store.state.authenticated">Edit</th> -->
    <th>Initials</th>
    <th v-if="$store.state.authenticated">Delete</th>
    <th>Complete Task</th>
    <th>Task Name</th>
    <th>Task Description</th>
    <th>Time Interval</th>
    <th>Guide</th>
    <tr v-for="(value, key) in json[selectedKey]" v-bind:key="key" v-bind:value="value">
      <!--<td v-if="$store.state.authenticated">
        <button classtype="submit" class="btn btn-success" @click="showModal = true">&#9998;</button>
      </td>-->
      <td>
        <span><p>AJ</p></span>
      </td>
      <td v-if="$store.state.authenticated">
          <button classtype="submit" class="btn btn-danger" @click="deleteItem(key)">x</button>
      </td>
      <td>
        <input class="task-table-checkbox" type="checkbox" @change="updateTaskStatus(key)" />
       <td>
         <span>{{ value.name }}</span>
         <div class="information-button"></div>
       </td>
       <td>
          <button v-if="!$store.state.authenticated" classtype="submit" class="btn btn-info" @click="showModal = true">?</button>
          <!-- make editable paragraph box -->
          <div v-if="$store.state.authenticated" contenteditable="true" @input="getInput(key)">
           <p>
              {{ value.description }}
           </p>
          </div>
        </td>
        <td>
          <button class="btn btn-success" @click="editSchedule(value)">Schedule</button>
        </td>
        <td>
          <button class="btn btn-info" @click="download(value.guide)">Download</button>
        </td>
    </tr>
    <!-- final row to enter new task information -->
    <tr v-if="$store.state.isCreatingNewTask">
      <td>
        <span><p v-bind:style="{ color: 'grey' }">AJ</p></span>
      </td>
      <td>
          <button classtype="submit" class="btn btn-secondary">x</button>
      </td>
      <td>
        <input class="task-table-checkbox" type="checkbox" @change="updateTaskStatus(key)"/>
       <td>
         <span contenteditable="true" @input="getTaskName()">
         </span>
       </td>
       <td>
          <!-- make editable paragraph box -->
          <span contenteditable="true" @input="getTaskDescription()">
          </span>
        </td>
        <td>
        </td>
    </tr>
</table>
<button classtype="submit" class="btn btn-info" @click="showReportsModal = true">Reports</button>
<button v-if="$store.state.authenticated" class="btn btn-secondary" @click="$store.state.isCreatingNewTask = true">Add A Task</button>
<button v-if="$store.state.isCreatingNewTask" class="btn btn-secondary" @click="createNewTask(taskName, taskDescription); $store.state.isCreateingNewTask = false">Create Task</button>
<button classtype="submit" class="btn btn-success" v-on:click="postDataToApi()">Submit Changes</button>
</div>
</template>
<script>

import reportsmodal from './ReportsModal'
import schedulemodal from './ScheduleModal'
import axios from 'axios'

export default {
  components: {
    reportsmodal,
    schedulemodal
  },
  data () {
    return {
      showModal: false,
      showReportsModal: false,
      taskName: '',
      taskDescription: '',
      selectedKey: '',
      showScheduleModal: false
    }
  },
  watch: {
    $route (to, from) {
      console.log(this.selectedKey)
      this.selectedKey = to.params.machineId
    }
  },
  created () {
    this.selectedKey = this.$route.params.machineId
  },
  beforeRouteUpdate (to, from, next) {
    this.selectedKey = to.params.machineId
    console.log(this.json)
    next()
  },
  computed: {
    taskArrayLength: function () {
      return Object.values(this.json[this.selectedKey]).length
    },
    // can't return prop of vue directly--need computed method
    returnMachineName: function () {
      return this.selectedKey
    },
    json: function () {
      return this.$store.getters.tasks
    }
  },
  methods: {
    submitClick () {
      console.log(Object.values(this.json[this.selectedKey])[0].completed)
    },
    // generate random number for unique key
    getRandomInteger () {
      return Math.floor(Math.random() * 10000) + 1
    },
    createNewTask (newTaskName, newTaskDescription) {
      var newTask = {}
      // assume we always have at least one task in the list -- fix later
      newTask.completed = false
      newTask.name = newTaskName
      newTask.description = newTaskDescription
      newTask.machine = this.selectedKey
      axios.post(`${process.env.BASE_URL}/tasks`, newTask)
        .then((response) => response.data)
        .then((response) => {
          console.log(response)
          this.$store.dispatch('clearCreatingNewTask')
          this.json[this.selectedKey][`key-${response.id}`] = response
          // use vue-simple-alert to notify user of successful submit
          this.$fire({
            title: 'Success',
            text: 'Data Successfully Submitted',
            type: 'success',
            timer: 3000
          })
        })
        .catch((error) => {
          console.log(error)
          this.$store.dispatch('clearCreatingNewTask')
          this.$alert('Oops there was an error', 'Failure', 'Error')
        })
    },
    updateTaskStatus (key) {
      this.json[this.selectedKey][key].completed = !this.json[this.selectedKey][key].completed
    },
    getInput (key) {
      this.json[this.selectedKey][key].description = event.target.innerText
      console.log(this.json[this.selectedKey][key].description)
    },
    emitSubmit () {
      this.$emit('payloadSubmitted', this.json)
      console.log('payload submitted')
    },
    deleteItem (task) {
      delete this.json[this.selectedKey][task]
    },
    getTaskName () {
      this.taskName = event.target.innerText
    },
    getTaskDescription () {
      this.taskDescription = event.target.innerText
    },
    postDataToApi () {
      axios.post(`${process.env.BASE_URL}/tasks`, this.json)
        .then((response) => {
          console.log(response)
          // use vue-simple-alert to notify user of successful submit
          this.$fire({
            title: 'Success',
            text: 'Data Successfully Submitted',
            type: 'success',
            timer: 3000
          })
        })
        .catch((error) => {
          console.log(error)
          this.$alert('Oops there was an error', 'Failure', 'Error')
        })
    },
    download (url) {
      axios.get(`${process.env.BASE_URL}/guides/${url}`, {
        responseType: 'blob'
      })
        .then(response => {
          console.log(response)
          const fileURL = window.URL.createObjectURL(new Blob([response.data]))
          const fileLink = document.createElement('a')
          fileLink.href = fileURL
          fileLink.setAttribute('download', 'file.pdf')
          document.body.appendChild(fileLink)
          fileLink.click()
        })
        .catch((error) => {
          console.log(error)
        })
    },
    editSchedule (value) {
      console.log(value)
      this.showScheduleModal = true
    },
    closeSchedule () {
      this.showScheduleModal = false
    }
  }
}
</script>
<style>
table>th{
  position: -webkit-sticky;
  position: sticky;
  top: 100px;
}
.task-table-checkbox{
    width:50px;
    height:50px;
}
.task-table{
    caption-side:top;
}
.information-button{
  padding-left:30px
}
</style>

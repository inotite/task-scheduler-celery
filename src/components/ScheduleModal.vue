<template>
<div id="schedule-modal">
  <div class="modal-mask">
    <div class="modal-wrapper">
      <div class="modal-container">
        <h3> Schedule </h3>
        <div class="row">
          <div class="col-3">
            <div class="form-group row">
              <div class="col-12 text-left">
                <input type="checkbox" id="daily" v-model="daily">
                <label for="daily">Daily</label>
              </div>
              <div class="col-12 text-left">
                <input type="checkbox" id="monthly" v-model="monthly">
                <label for="monthly">Monthly</label>
              </div>
            </div>
          </div>
          <div class="col-3">
            <div class="form-group row">
              <div class="col-12 text-left">
                <input type="checkbox" id="monday" v-model="monday" :disabled="!daily">
                <label for="monday">Monday</label>
              </div>
              <div class="col-12 text-left">
                <input type="checkbox" id="tuesday" v-model="tuesday" :disabled="!daily">
                <label for="tuesday">Tuesday</label>
              </div>
              <div class="col-12 text-left">
                <input type="checkbox" id="wednesday" v-model="wednesday" :disabled="!daily">
                <label for="wednesday">Wednesday</label>
              </div>
              <div class="col-12 text-left">
                <input type="checkbox" id="thursday" v-model="thursday" :disabled="!daily">
                <label for="thursday">Thursday</label>
              </div>
              <div class="col-12 text-left">
                <input type="checkbox" id="friday" v-model="friday" :disabled="!daily">
                <label for="friday">Friday</label>
              </div>
            </div>
          </div>
          <div v-if="daily && (monday || tuesday || wednesday || thursday || friday)" class="col-6">
            <label class="typo__label text-left">Hourly</label>
            <multiselect v-model="hours" :options="hourlyOptions" :multiple="true" :close-on-select="false" :preserve-search="true" label="name" track-by="name" placeholder="Select time" :preselect-first="true">
            </multiselect>
          </div>
        </div>
        <div v-if="monthly" class="row">
          <div class="col-12">
            <label class="typo__label text-left">Monthly</label>
            <multiselect v-model="months" :options="monthlyOptions" :multiple="true" :close-on-select="false" :preserve-search="true" label="name" track-by="name" placeholder="Select time" :preselect-first="true">
            </multiselect>
          </div>
        </div>
        <div class="row mt-3">
          <div class="col-12">
            <button classtype="submit" class="btn btn-danger" v-on:click="onClose">Close</button>
            <button classtype="submit" class="btn btn-success" v-on:click="onSave">Save</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>

import Multiselect from 'vue-multiselect'
import axios from 'axios'

export default {
  components: {
    Multiselect
  },
  name: 'ScheduleModal',
  data () {
    return {
      daily: true,
      monthly: false,
      monday: false,
      tuesday: false,
      wednesday: false,
      thursday: false,
      friday: false,
      hours: [],
      hourlyOptions: [
        { name: '0:00' },
        { name: '1:00' },
        { name: '2:00' },
        { name: '3:00' },
        { name: '4:00' },
        { name: '5:00' },
        { name: '6:00' },
        { name: '7:00' },
        { name: '8:00' },
        { name: '9:00' },
        { name: '10:00' },
        { name: '11:00' },
        { name: '12:00' },
        { name: '13:00' },
        { name: '14:00' },
        { name: '15:00' },
        { name: '16:00' },
        { name: '17:00' },
        { name: '18:00' },
        { name: '19:00' },
        { name: '20:00' },
        { name: '21:00' },
        { name: '22:00' },
        { name: '23:00' }
      ],
      months: [],
      monthlyOptions: [
        { name: 'January' },
        { name: 'February' },
        { name: 'March' },
        { name: 'April' },
        { name: 'May' },
        { name: 'June' },
        { name: 'July' },
        { name: 'August' },
        { name: 'September' },
        { name: 'October' },
        { name: 'November' },
        { name: 'December' }
      ]
    }
  },
  props: {
    id: Number,
    schedule: Object
  },
  created () {
    console.log(this.schedule)
    if (this.schedule) {
      this.hours = this.schedule.hour.split(',').map(hour => this.hourlyOptions[hour])
      if (this.schedule.day_of_week === '*') {
        this.monday = this.tuesday = this.wednesday = this.thursday = this.friday = true
      } else {
        const days = this.schedule.day_of_week.split(',')
        this.monday = days.includes('0')
        this.tuesday = days.includes('1')
        this.wednesday = days.includes('2')
        this.thursday = days.includes('3')
        this.friday = days.includes('4')
      }
      if (this.schedule.month_of_year === '*') {
        this.months = []
        this.monthly = false
      } else {
        this.monthly = true
        this.months = this.schedule.month_of_year.split(',').map(month => this.monthlyOptions[month])
      }
    }
  },
  methods: {
    onClose () {
      this.$emit('closeSchedule')
    },
    onSave () {
      console.log(this.hours)
      if ((!this.daily && !this.monthly) || (this.daily && this.hours.length === 0) || (this.monthly && this.months.length === 0)) {
        this.$alert('Your schedule option is invalid!', 'Invalid option', 'error')
        return
      }
      const hours = this.hours.map(
        hour => this.hourlyOptions.findIndex((option) => option.name === hour.name)
      )
      const months = this.months.map(
        month => this.monthlyOptions.findIndex((option) => option.name === month.name)
      )
      const day = `${this.monday ? '0,' : ''}${this.tuesday ? '1,' : ''}${this.wednesday ? '2,' : ''}${this.thursday ? '3,' : ''}${this.friday ? '4' : ''}`
      const cron = {
        hour: hours.join(','),
        day_of_week: (!this.daily ? '*' : day.replace(/,*$/, '')),
        month_of_year: (!this.monthly ? '*' : months.join(','))
      }

      axios.put(`${process.env.BASE_URL}/tasks/${this.id}`, {
        schedule: cron
      })
        .then(response => {
          console.log(response)
          this.$emit('closeSchedule')
        })
        .catch(err => {
          console.error(err)
          this.$emit('closeSchedule')
        })
    }
  }
}
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
/* create some padding between modal title and content */
.modal-title{
  padding-bottom: 2em;
}
/* modal-mask makes the background opaque */
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
  width: 40rem;
  min-height: 20rem;
  background-color: white;
  /* pad inner text */
  padding: 20px 20px;
  /* centering modal */
  position: fixed;
  left: calc(50% - 20rem);
  top: 50%;
  /* border:1px solid; */
  -webkit-transform:translateY(-50%);
  -moz-transform:translateY(-50%);
  -ms-transform:translateY(-50%);
  -o-transform:translateY(-50%);
  transform:translateY(-50%);
}
.typo__label {
  font-family: Lato,sans-serif;
  display: block;
  font-weight: 400;
  font-size: .875rem;
  margin: .625rem 0;
}
#schedule-modal .form-group {
  margin-bottom: 0;
}
</style>

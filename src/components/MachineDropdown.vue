<template>
<div class="form-group">
<a>
<label>Select Machine</label>
<select class="form-control" v-model="selected" v-on:change="getSelectedMachine(selected); $store.state.isCreatingNewTask = false" aria-valuetext="Select Machine">
  <option class="dropdown-content" v-for="key in Object.keys(options)" v-bind:key="key"><a> {{ key }} </a></option>
  </select>
</a>
</div>
</template>
<script>
export default {
  props: {
    options: Object
  },
  data () {
    return {
      selected: ''
    }
  },
  methods: {
    getSelectedMachine (selected) {
      this.$emit('keySelected', selected)
      console.log('here')
    }
  }
}
</script>
<style>
html {
  font-family: sans-serif;
  -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
}
body {
  margin: 0;
}
/* table and rows */
table {
  padding-top: 100px;
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}
table td, table th {
  border: 1px solid #ddd;
  padding: 8px;
}
table tr:nth-child(even){background-color: #f2f2f2;}
table tr:hover {background-color: #ddd;}
table caption{
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: center;
  background-color: #1d1e20;
  color: white;
}
table th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: center;
  background-color: #1d1e20;
  color: white;
}
.dropdown{
    position: relative;
    display: inline-block;
    float: left;
    border: hidden;
    background:#ffd503;
}
.dropdown-content{
  background:#f2f2f2;
}
li.dropdown{
    display: inline-block;
}
.dropdown-content{
    display: none;
    position: absolute;
    list-style-type: none;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
}
.dropdown:hover .dropdown-content{
    display: block;
 }
.dropdown-content a {
    padding: 0px 0px;
    text-decoration: none;
    border: 1px solid white;
    display: block;
    }
.hide {
  display: none;
}

</style>

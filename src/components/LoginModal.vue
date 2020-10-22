<template>
  <div id="modal">
      <div class="modal-mask">
          <div class="modal-wrapper">
            <div class="modal-container">
              <div class="modal-title">
                  <h3> Login </h3>
               </div>
               <form>
                <div class="form-group row">
                    <div class="col-sm-10 mx-auto">
                        <input type="text" name="username" v-model="username" placeholder="Username" />
                    </div>
                </div>
               <div class="form-group row">
                   <div class="col-sm-10 mx-auto">
                      <input type="password" name="password" v-model="password" placeholder="Password" />
                   </div>
               </div>
            </form>
            <div class="row">
              <div class="col-md-4 mx-auto">
                <button class="btn btn-success" v-on:click="login()">Login</button>
              </div>
              <div class="col-md-4 mx-auto">
                <button classtype="submit" class="btn btn-danger" v-on:click="$parent.showLoginModal = false">Close</button>
                </div>
            </div>
          </div>
      </div>
   </div>
</div>
</template>
<script>
export default{
  name: 'MachineInfoModal',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login () {
      console.log(this.username)
      if (this.username !== '' && this.password !== '') {
        if (this.username === this.$parent.mockAccount.username && this.password === this.$parent.mockAccount.password) {
          // set store authenticated value to true
          this.$store.commit('setAuthenticated')
          // reroute to root
          this.$router.replace('/')
          // close the modal
          this.$parent.showLoginModal = false
        } else {
          console.log('The username / password is incorrect')
        }
      } else {
        console.log('Must enter a valid username / password')
      }
    }
  }
}
</script>
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
    width: 25em;
    /* min-height: 15em; */
    background-color: white;
    /* pad inner text */
    padding: 10px 10px;
    /* centering modal */
    position: fixed;
    left: 40%;
    top: 50%;
    border:1px solid;
    -webkit-transform:translateY(-50%);
    -moz-transform:translateY(-50%);
    -ms-transform:translateY(-50%);
    -o-transform:translateY(-50%);
    transform:translateY(-50%);
}
</style>

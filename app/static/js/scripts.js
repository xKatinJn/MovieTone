
var app = new Vue({
	el:'#app',
	data: {
		isClose: false,
		leftMRPanel: '0',
	
	},
	methods :{
		menyOpen: function(){
			this.isClose = true;
		},
		menyClose: function(){
			this.isClose = false;
		},
		goToRegistr: function(){
			this.leftMRPanel = '-200%';
		},
		goToVhod: function(){
			this.leftMRPanel = '0%';
		}
	}
	
});

<template>
	<div class="className">
		<el-card>
			<div class="title">
				微情感分析演示
			</div>
			<div class="tip">
				请输入要进行微情感分析的文本:
			</div>
			<el-input v-model="textarea" type="textarea" :rows="7" placeholder="请输入要进行微情感分析的文本" />
			<div>
				<el-button class="el-button" slot="trigger" icon="el-icon-help" size="medium" type="primary"
					@click="post_analyse()" round>
					微情感分析
				</el-button>
			</div>
			<div ref="analy" class="result">情感类别：{{label}} </div>
			<div align="center">
				<el-image style="img" :src="url">
				</el-image>
			</div>
		</el-card>
	</div>
</template>

<script>
	import axios from "axios";
	export default {
		data() {
			return {
				textarea: '',
				show: 'hidden',
				label: '',
				url: '/src/assets/demo.png'
			}
		},
		methods: {
			post_analyse() {
				var that = this;
				var context = that.textarea; // 获取输入框的文本
				if (context == '') {
					this.$message({
						showClose: true,
						message: '输入文本内容不能为空',
						type: 'warning'
					});
					that.label = '';
					that.$refs.analy.style.visibility = 'hidden'
				} else {
					axios.post('http://127.0.0.1:5000/emoAnalysis', {
						text: that.textarea,
					}).then((response) => {
						console.log(response);
						console.log(response.data);
						that.label = response.data.label;
						that.$refs.analy.style.visibility = 'visible'
						that.$message({
							showClose: true,
							message: '微情感分析完成！情感类别:' + that.label,
							type: 'success'
						});
					}).catch((error) => {
						console.log(error);
						that.$message({
							showClose: true,
							message: '请求出错！',
							type: 'error'
						});
					});
				}
			},
			get_analyse() {
				var that = this;
				var context = that.textarea; // 获取输入框的文本
				if (context == '') {
					this.$message({
						showClose: true,
						message: '输入文本内容不能为空',
						type: 'warning'
					});
					that.label = '';
					that.$refs.analy.style.visibility = 'hidden'
				} else {
					axios.get('http://127.0.0.1:5000/emoAnalysis', {
							params: {
								text: context
							}
						})
						.then(function(response) {
							console.log(response);
							console.log(response.data);
							that.label = response.data.label;
							that.$refs.analy.style.visibility = 'visible'
							that.$message({
								showClose: true,
								message: '微情感分析完成！情感类别:'+that.label,
								type: 'success'
							});
						})
						.catch(function(error) {
							console.log(error);
							that.$message({
								showClose: true,
								message: '请求出错！',
								type: 'error'
							});
						});
				}
			}
		}
	}
</script>

<style scoped>
	.title {
		font-family: 黑体;
		font-size: 30px;
		font-weight: bold;
		margin: 0 auto;
		width: 220px;
		height: 35px;
		margin-bottom: 10px;
	}

	.tip {
		font-family: 宋体;
		font-size: 18px;
		font-weight: bold;
		margin-bottom: 10px;
	}

	.el-button {
		margin: 0 auto;
		position: relative;
		margin-top: 15px;
		margin-bottom: 10px;
		display: block;
	}

	.result {
		font-family: 宋体;
		font-size: 22px;
		font-weight: bold;
		/* padding-top: 10px;
		padding-bottom: 15px; */
		margin: 0 auto;
		margin-top: 15px;
		margin-bottom: 15px;
		width: 160px;
		height: 25px;
		color: #4876FF;
		visibility: hidden;
	}
</style>

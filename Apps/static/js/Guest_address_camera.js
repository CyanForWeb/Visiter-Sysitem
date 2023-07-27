Vue.createApp({
        data() {
            return {
                video: null,
                canvas: null,
                context: null,
                dataUrl: '',
                status: 'none'
            }
        },
        methods: {
            // ① カメラとキャンバスの準備
            initialize() {
                this.status = 'initialize';
                navigator.mediaDevices.getUserMedia({
                    video: {
                        facingMode: {
                            ideal: 'environment'
                        }
                    }
                })
                .then(stream => {
                    this.canvas = this.$refs.canvas;
                    this.context = this.canvas.getContext('2d');
                    this.video = document.createElement('video');
                    this.video.addEventListener('loadedmetadata', () => { // メタデータが取得できるようになったら実行
                        const canvasContainer = this.$refs['canvas-container'];
                        this.canvas.width = canvasContainer.offsetWidth;
                        this.canvas.height = parseInt(this.canvas.width * this.video.videoHeight / this.video.videoWidth);
                        this.render();
                    });
                    // iOSのために以下３つの設定が必要
                    this.video.setAttribute('autoplay', '');
                    this.video.setAttribute('muted', '');
                    this.video.setAttribute('playsinline', '');
                    this.video.srcObject = stream;
                    this.playVideo();
                })
                .catch(error => console.log(error));
            },
            render() {
                if(this.video.readyState === this.video.HAVE_ENOUGH_DATA) {
                    this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
                }
                requestAnimationFrame(this.render);
            },
            runOcr() { // ③ スナップショットからテキストを抽出
                this.status = 'reading';
                Tesseract.recognize(this.dataUrl, 'jpn',{
                    logger: log => {
                        console.log(log);
                    }
                })
                .then(result => {
                  const str = result.data.text;
                  console.log(str);
                  const name = 'あ'; //ここに住人の名前を入れる
                  const result_name = str.includes(name);
                  if(result_name==true){
                    //次の画面に行く
                    if(status=='delivery_stamp'){
                      //住民に通知機能
                    }
                    location.href = url;
                  }else{
                    //読み取りアラートを出す
                    const message = '正常に読み取れませんでした。\n再度読み取りを実行するか、\n来訪目的の選択画面に戻り、「その他」から手続きを行ってください。';
                    alert(message);
                  }
                })
                .catch(error => console.log(error))
                .finally(() => {
                    this.playVideo();
                });
            },
            playVideo() {
                this.video.play();
                this.status = 'play';
            },
            pauseVideo() {
                this.video.pause();
                this.status = 'pause';
            },
            takeSnapshot() { // ② スナップショットを取る（カメラは一時停止）
                this.pauseVideo();
                this.dataUrl = this.canvas.toDataURL();
                if(this.status == 'pause'){
                  this.runOcr();//文字を読み取る
                }
            },
        },
        mounted() {
            this.initialize();
        }
      }).mount('#app');

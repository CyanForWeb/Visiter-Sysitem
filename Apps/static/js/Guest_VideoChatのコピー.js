const { nowInSec, SkyWayAuthToken, SkyWayContext, SkyWayRoom, SkyWayStreamFactory, uuidV4 } = skyway_room;

const token = new SkyWayAuthToken({
  jti: uuidV4(),
  iat: nowInSec(),
  exp: nowInSec() + 60 * 60 * 24,
  scope: {
    app: {
      id: '2ffe76bb-d2b4-4f1b-88fa-934d2174e00a',
      turn: true,
      actions: ['read'],
      channels: [
        {
          id: '*',
          name: '*',
          actions: ['write'],
          members: [
            {
              id: '*',
              name: '*',
              actions: ['write'],
              publication: {
                actions: ['write'],
              },
              subscription: {
                actions: ['write'],
              },
            },
          ],
          sfuBots: [
            {
              actions: ['write'],
              forwardings: [
                {
                  actions: ['write'],
                },
              ],
            },
          ],
        },
      ],
    },
  },
}).encode('h2EJA53oF6yRNdzuYXWeaoRbyTBWHsRD0oiyx/FzZWM=');

(async () => {
  const joinButton = document.getElementById('join');

  const message = document.getElementById('message');
  const joiningMsg = document.getElementById('joining');
  joiningMsg.innerText = "住人が 通話 を希望しています\n応答ボタンを押してください";
  //const closeButton = document.getElementById('close');
  //closeButton.style.display = "none";//none=非表示
  const videoChat = document.getElementById('videoChat');
  videoChat.style.display = "block";//block=表示する

  const video = await SkyWayStreamFactory.createCameraVideoStream();
  const localVideo = document.getElementById('local-video');
  video.attach(localVideo);
  await localVideo.play();//videoタグでカメラのプレビューが見られるようにする
  const audio = await SkyWayStreamFactory.createMicrophoneAudioStream();


  joinButton.onclick = async () => {
    joinButton.style.display = "none";//参加ボタンを非表示にする
    joiningMsg.innerText = "通話 待機中...";//...というメッセージを表示する
    //closeButton.style.display = "block";//退出ボタンを表示する
    //message.style.display = "none";//参加しましょうor参加ボタンを押してくださいメッセージを非表示にする

    const context = await SkyWayContext.Create(token);
    const room = await SkyWayRoom.FindOrCreate(context, {
      type: 'p2p',
      name: 'VideoRoom',
    });
    const me = await room.join();

    //動画/音声の送信を開始
    await me.publish(audio);
    await me.publish(video);

    //相手の映像と音声をsubscribeする
    const subscribeAndAttach = async (publication) => {
      if (publication.publisher.id === me.id) return;

      const { stream } = await me.subscribe(publication.id);
      joiningMsg.innerText = "通話が開始しました";//メッセージを表示する


      switch (stream.contentType) {
        case 'video':
          {
            const elm = document.getElementById('partner_video');
            elm.playsInline = true;
            elm.autoplay = true;
            stream.attach(elm);
          }
          break;
        case 'audio':
          {
            const elm = document.getElementById('partner_audio');
            //elm.controls = true;
            elm.autoplay = true;
            stream.attach(elm);
          }
          break;
        }
    };

    room.publications.forEach(subscribeAndAttach);
    room.onStreamPublished.add((e) => subscribeAndAttach(e.publication));
  };

  //closeButton.onclick = async () => {
  //  videoChat.style.display = "none";//チャットエリアを非表示にする
  //};

})();

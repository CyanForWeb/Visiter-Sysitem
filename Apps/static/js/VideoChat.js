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

document.addEventListener('DOMContentLoaded', function() {
    const videoToggle = document.getElementById('videoToggle');
    const localVideo = document.getElementById('local-video');
    const status = document.getElementById('status');

    videoToggle.addEventListener('change', function() {
      if (this.checked) {
        localVideo.style.display = 'block';
        status.textContent = 'カメラ ON';
      } else {
        localVideo.style.display = 'none';
        status.textContent = 'カメラ OFF';
      }
    });
  });

(async () => {
  const localVideo = document.getElementById('local-video');
  const buttonArea = document.getElementById('button-area');
  const remoteMediaArea = document.getElementById('remote-media-area');
  const roomNameInput = document.getElementById('room-name');

  const myId = document.getElementById('my-id');
  const joinButton = document.getElementById('join');

  const message = document.getElementById('message');
  const joiningMsg = document.getElementById('joining');
  joiningMsg.style.display = "none";//none=非表示
  const closeButton = document.getElementById('close');
  closeButton.style.display = "none";//none=非表示
  const videoChat = document.getElementById('videoChat');
  videoChat.style.display = "block";//block=表示する

  const { audio, video } =
    await SkyWayStreamFactory.createMicrophoneAudioAndCameraStream();
  video.attach(localVideo);
  await localVideo.play();

  joinButton.onclick = async () => {
    joinButton.style.display = "none";//参加ボタンを非表示にする
    joiningMsg.style.display = "block";//参加中...というメッセージを表示する
    closeButton.style.display = "block";//終了ボタンを表示する
    message.style.display = "none";//参加しましょうメッセージを非表示にする

    const context = await SkyWayContext.Create(token);
    const room = await SkyWayRoom.FindOrCreate(context, {
      type: 'p2p',
      name: roomNameInput.value,
    });
    const me = await room.join();

    //myId.textContent = me.id;

    await me.publish(audio);
    await me.publish(video);

    //ここから
    //相手の映像と音声をsubscribeする
    const subscribeAndAttach = (publication) => {
      if (publication.publisher.id === me.id) return;

      const subscribeButton = document.createElement('button');

      subscribeButton.textContent = `参加者の ${publication.contentType} を表示　`;
      buttonArea.appendChild(subscribeButton);

      subscribeButton.onclick = async () => {
        const { stream } = await me.subscribe(publication.id);

        //let newMedia;
        switch (stream.contentType) {
        //switch (stream.track.kind) {
          case 'video':
            //newMedia = document.createElement('video');
            //newMedia.playsInline = true;
            //newMedia.autoplay = true;
            {
            const elm = document.createElement('video');
            elm.playsInline = true;
            elm.autoplay = true;
            stream.attach(elm);
            remoteMediaArea.appendChild(elm);
            }
            break;
          case 'audio':
            //newMedia = document.createElement('audio');
            //newMedia.controls = true;
            //newMedia.autoplay = true;
            {
            const elm = document.createElement('audio');
            //elm.controls = true;
            elm.autoplay = true;
            stream.attach(elm);
            remoteMediaArea.appendChild(elm);
            }
            break;
          //default:
          //  return;
        }
        //stream.attach(newMedia);
        //remoteMediaArea.appendChild(newMedia);
      };
    };
    //ここまで

    room.publications.forEach(subscribeAndAttach);
    room.onStreamPublished.add((e) => subscribeAndAttach(e.publication));
  };

  closeButton.onclick = async () => {
    videoChat.style.display = "none";//チャットエリアを非表示にする
  };

})();

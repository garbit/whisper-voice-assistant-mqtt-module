export ROOT=$(pwd)
export MODULES=$ROOT/modules

cd $MODULES/whisper-voice-assistant
docker build -t whisper-voice-assistant .
cd $ROOT

cd $MODULES/subscriber
docker build -t subscriber .
cd $ROOT

docker-compose up -d mqtt whisper-voice-assistant subscriber
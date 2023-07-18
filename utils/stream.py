import pyaudio


class InitStreamException(BaseException):
    pass


class Stream:
    def __init__(self, channels: int = None, rate: int = None, chunk: int = None, input_device: int = None):
        try:
            if not all([channels, rate, chunk, input_device]): raise InitStreamException('Not all arguments were given')
            self._channels = channels
            self._rate = rate
            self._chunk = chunk
            self._input_device = input_device
            self._stream = pyaudio.PyAudio.open(
                format=pyaudio.paFloat32,
                channels=channels,
                rate=rate,
                input=True,
                output=False,
                frames_per_buffer=chunk,
                input_device_index=input_device
            )
        except InitStreamException as e:
            print(e)

    @property
    def channels(self) -> str:
        return str(self._channels)

    @property
    def rate(self) -> str:
        return str(self._rate)

    @property
    def chunk(self) -> str:
        return str(self._chunk)

    @property
    def input_device(self) -> str:
        return str(self._input_device)

    @property
    def stream(self):
        return self._stream

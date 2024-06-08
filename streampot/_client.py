import requests
from dataclasses import dataclass
from typing import Optional
from enum import Enum
import time


class JobStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    UPLOADING = "uploading"


@dataclass
class JobEntity:
    id: int
    status: JobStatus
    created_at: str
    logs: Optional[str] = None
    outputs: Optional[dict] = None
    completed_at: Optional[str] = None


def _response_to_job(data: dict) -> JobEntity:
    data['status'] = JobStatus[data['status'].upper()]
    return JobEntity(**data)


class StreamPotClient:
    def __init__(self, secret: str, base_url: str = 'https://api.streampot.io/v1'):
        self.secret = secret
        self.base_url = base_url
        self.actions = []

    def get_job(self, job_id: int) -> JobEntity:
        response = requests.get(f"{self.base_url}/jobs/{job_id}", headers=self._auth_header())
        response.raise_for_status()

        return _response_to_job(response.json())

    def run(self) -> JobEntity:
        response = requests.post(f"{self.base_url}/", headers=self._auth_header(), json=self.actions)
        response.raise_for_status()

        return _response_to_job(response.json())

    def run_and_wait(self, interval_ms: int = 1000) -> JobEntity:
        job = self.run()
        while job.status not in [JobStatus.COMPLETED, JobStatus.FAILED]:
            time.sleep(interval_ms / 1000)
            job = self.get_job(job.id)
        return job

    def _auth_header(self) -> dict:
        return {
            "Authorization": f"Bearer {self.secret}",
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }

    def _add_action(self, name: str, *values):
        self.actions.append({"name": name, "value": list(values)})
        return self

    def merge_add(self, source: str):
        return self._add_action('mergeAdd', source)

    def add_input(self, source: str):
        return self._add_action('addInput', source)

    def input(self, source: str):
        return self._add_action('input', source)

    def with_input_format(self, format_name: str):
        return self._add_action('withInputFormat', format_name)

    def input_format(self, format_name: str):
        return self._add_action('inputFormat', format_name)

    def from_format(self, format_name: str):
        return self._add_action('fromFormat', format_name)

    def with_input_fps(self, fps: int):
        return self._add_action('withInputFps', fps)

    def with_fps_input(self, fps: int):
        return self._add_action('withFpsInput', fps)

    def input_fps(self, fps: int):
        return self._add_action('inputFPS', fps)

    def fps_input(self, fps: int):
        return self._add_action('fpsInput', fps)

    def native_framerate(self):
        return self._add_action('nativeFramerate')

    def with_native_framerate(self):
        return self._add_action('withNativeFramerate')

    def native(self):
        return self._add_action('native')

    def set_start_time(self, seek):
        return self._add_action('setStartTime', seek)

    def seek_input(self, seek):
        return self._add_action('seekInput', seek)

    def loop(self, duration=None):
        return self._add_action('loop', duration)

    def with_no_audio(self):
        return self._add_action('withNoAudio')

    def no_audio(self):
        return self._add_action('noAudio')

    def with_audio_codec(self, codec: str):
        return self._add_action('withAudioCodec', codec)

    def audio_codec(self, codec: str):
        return self._add_action('audioCodec', codec)

    def with_audio_bitrate(self, bitrate):
        return self._add_action('withAudioBitrate', bitrate)

    def audio_bitrate(self, bitrate):
        return self._add_action('audioBitrate', bitrate)

    def with_audio_channels(self, channels: int):
        return self._add_action('withAudioChannels', channels)

    def audio_channels(self, channels: int):
        return self._add_action('audioChannels', channels)

    def with_audio_frequency(self, freq: int):
        return self._add_action('withAudioFrequency', freq)

    def audio_frequency(self, freq: int):
        return self._add_action('audioFrequency', freq)

    def with_audio_quality(self, quality: int):
        return self._add_action('withAudioQuality', quality)

    def audio_quality(self, quality: int):
        return self._add_action('audioQuality', quality)

    def with_audio_filter(self, filters):
        return self._add_action('withAudioFilter', filters)

    def with_audio_filters(self, filters):
        return self._add_action('withAudioFilters', filters)

    def audio_filter(self, filters):
        return self._add_action('audioFilter', filters)

    def audio_filters(self, filters):
        return self._add_action('audioFilters', filters)

    def with_no_video(self):
        return self._add_action('withNoVideo')

    def no_video(self):
        return self._add_action('noVideo')

    def with_video_codec(self, codec: str):
        return self._add_action('withVideoCodec', codec)

    def video_codec(self, codec: str):
        return self._add_action('videoCodec', codec)

    def with_video_bitrate(self, bitrate, constant=None):
        return self._add_action('withVideoBitrate', bitrate, constant)

    def video_bitrate(self, bitrate, constant=None):
        return self._add_action('videoBitrate', bitrate, constant)

    def with_video_filter(self, filters):
        return self._add_action('withVideoFilter', filters)

    def with_video_filters(self, filters):
        return self._add_action('withVideoFilters', filters)

    def video_filter(self, filters):
        return self._add_action('videoFilter', filters)

    def video_filters(self, filters):
        return self._add_action('videoFilters', filters)

    def with_output_fps(self, fps: int):
        return self._add_action('withOutputFps', fps)

    def with_fps_output(self, fps: int):
        return self._add_action('withFpsOutput', fps)

    def with_fps(self, fps: int):
        return self._add_action('withFps', fps)

    def output_fps(self, fps: int):
        return self._add_action('outputFPS', fps)

    def fps_output(self, fps: int):
        return self._add_action('fpsOutput', fps)

    def fps(self, fps: int):
        return self._add_action('fps', fps)

    def take_frames(self, frames: int):
        return self._add_action('takeFrames', frames)

    def with_frames(self, frames: int):
        return self._add_action('withFrames', frames)

    def frames(self, frames: int):
        return self._add_action('frames', frames)

    def keep_pixel_aspect(self):
        return self._add_action('keepPixelAspect')

    def keep_display_aspect(self):
        return self._add_action('keepDisplayAspect')

    def keep_display_aspect_ratio(self):
        return self._add_action('keepDisplayAspectRatio')

    def keep_dar(self):
        return self._add_action('keepDAR')

    def with_size(self, size: str):
        return self._add_action('withSize', size)

    def set_size(self, size: str):
        return self._add_action('setSize', size)

    def size(self, size: str):
        return self._add_action('size', size)

    def with_aspect(self, aspect):
        return self._add_action('withAspect', aspect)

    def with_aspect_ratio(self, aspect):
        return self._add_action('withAspectRatio', aspect)

    def set_aspect(self, aspect):
        return self._add_action('setAspect', aspect)

    def set_aspect_ratio(self, aspect):
        return self._add_action('setAspectRatio', aspect)

    def aspect(self, aspect):
        return self._add_action('aspect', aspect)

    def aspect_ratio(self, aspect):
        return self._add_action('aspectRatio', aspect)

    def apply_autopadding(self, pad, color):
        return self._add_action('applyAutopadding', pad, color)

    def apply_auto_padding(self, pad, color):
        return self._add_action('applyAutoPadding', pad, color)

    def apply_autopad(self, pad, color):
        return self._add_action('applyAutopad', pad, color)

    def apply_auto_pad(self, pad, color):
        return self._add_action('applyAutoPad', pad, color)

    def with_autopadding(self, pad, color):
        return self._add_action('withAutopadding', pad, color)

    def with_auto_padding(self, pad, color):
        return self._add_action('withAutoPadding', pad, color)

    def with_autopad(self, pad, color):
        return self._add_action('withAutopad', pad, color)

    def with_auto_pad(self, pad, color):
        return self._add_action('withAutoPad', pad, color)

    def auto_pad(self, pad, color):
        return self._add_action('autoPad', pad, color)

    def autopad(self, pad, color):
        return self._add_action('autopad', pad, color)

    def add_output(self, target: str):
        return self._add_action('addOutput', target)

    def output(self, target: str):
        return self._add_action('output', target)

    def seek_output(self, seek):
        return self._add_action('seekOutput', seek)

    def seek(self, seek):
        return self._add_action('seek', seek)

    def with_duration(self, duration):
        return self._add_action('withDuration', duration)

    def set_duration(self, duration):
        return self._add_action('setDuration', duration)

    def duration(self, duration):
        return self._add_action('duration', duration)

    def to_format(self, format_name: str):
        return self._add_action('toFormat', format_name)

    def with_output_format(self, format_name: str):
        return self._add_action('withOutputFormat', format_name)

    def output_format(self, format_name: str):
        return self._add_action('outputFormat', format_name)

    def format(self, format_name: str):
        return self._add_action('format', format_name)

    def map(self, spec: str):
        return self._add_action('map', spec)

    def update_flv_metadata(self):
        return self._add_action('updateFlvMetadata')

    def flvmeta(self):
        return self._add_action('flvmeta')

    def add_input_option(self, *options):
        return self._add_action('addInputOption', *options)

    def with_input_options(self, *options):
        return self._add_action('withInputOptions', *options)

    def with_input_option(self, *options):
        return self._add_action('withInputOption', *options)

    def input_option(self, *options):
        return self._add_action('inputOption', *options)

    def add_input_options(self, *options):
        return self._add_action('addInputOptions', *options)

    def add_output_option(self, *options):
        return self._add_action('addOutputOption', *options)

    def add_output_options(self, *options):
        return self._add_action('addOutputOptions', *options)

    def add_option(self, *options):
        return self._add_action('addOption', *options)

    def with_output_option(self, *options):
        return self._add_action('withOutputOption', *options)

    def with_output_options(self, *options):
        return self._add_action('withOutputOptions', *options)

    def with_option(self, *options):
        return self._add_action('withOption', *options)

    def with_options(self, *options):
        return self._add_action('withOptions', *options)

    def output_option(self, *options):
        return self._add_action('outputOption', *options)

    def output_options(self, *options):
        return self._add_action('outputOptions', *options)

    def filter_graph(self, spec, map=None):
        return self._add_action('filterGraph', spec, map)

    def complex_filter(self, spec, map=None):
        return self._add_action('complexFilter', spec, map)

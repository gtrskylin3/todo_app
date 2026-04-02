# src/presentation/widgets/lofi_player.py
import logging
from PyQt6.QtCore import QUrl, Qt, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QSlider
from PyQt6.QtCore import pyqtSignal

logger = logging.getLogger(__name__)


class LofiPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.lofi_player = QMediaPlayer()
        
        # Создаём QAudioOutput с текущим устройством по умолчанию
        self._update_audio_output()

        self.is_playing = False
        self.is_loading = False
        self.stream_url = QUrl("https://live.lofiradio.ru/lofi_mp3_128")

        self._setup_ui()
        self._connect_signals()
        self.media_devices = QMediaDevices()
        self.media_devices.audioOutputsChanged.connect(self._on_audio_devices_changed)

    def _update_audio_output(self):
        """Обновить QAudioOutput с текущим устройством по умолчанию"""
        device = QMediaDevices.defaultAudioOutput()
        self.audio_output = QAudioOutput(device)
        self.audio_output.setVolume(0.05)  # 50% громкость по умолчанию
        self.lofi_player.setAudioOutput(self.audio_output)
        logger.info(f"Audio output set to: {device.description()}")

    def _on_audio_devices_changed(self):
        logger.info("Audio devices changed, updating output...")
        
        was_playing = self.is_playing

        self.lofi_player.stop()
        self._update_audio_output()

        if was_playing:
            self.lofi_player.setSource(self.stream_url)
            self.lofi_player.play()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Ползунок громкости (скрыт по умолчанию) - сверху
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setObjectName("lofiVolumeSlider")
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(20)
        self.volume_slider.setValue(5)  # 50% по умолчанию
        self.volume_slider.setFixedWidth(90)  # Компактный размер
        self.volume_slider.setFixedHeight(20)
        self.volume_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.volume_slider.setVisible(False)
        layout.addWidget(self.volume_slider, alignment=Qt.AlignmentFlag.AlignRight)

        # Кнопка - снизу
        self.button = QPushButton("🎵", self)
        self.button.setObjectName("lofiButton")
        self.button.setCheckable(True)
        self.button.setFixedSize(90, 36)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignRight)

        # Фиксированный размер для всего виджета
        self.setFixedSize(90, 64)  # 90 (ширина) x (36 + 4 + 20 + 4 margin)

    def _connect_signals(self):
        self.button.clicked.connect(self.toggle)
        self.lofi_player.playbackStateChanged.connect(self._on_playback_state_changed)
        self.lofi_player.errorOccurred.connect(self._on_error)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)

    def _on_volume_changed(self, value: int):
        """Изменение громкости"""
        volume = value / 150
        self.audio_output.setVolume(volume)
        logger.debug(f"Volume changed to {value}%")

    def toggle(self):
        if self.is_loading:
            return

        if not self.is_playing:
            self._start_playing()
        else:
            self._stop_playing()

    def _start_playing(self):
        self.is_loading = True
        self.button.setText("🎵")
        self.button.setEnabled(False)

        logger.info("Starting LoFi stream...")

        self.lofi_player.setSource(self.stream_url)
        self.lofi_player.play()

    def _stop_playing(self):
        self.lofi_player.stop()
        self._on_stopped()

    def _on_playback_state_changed(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.is_playing = True
            self.is_loading = False
            self.button.setText("⏸️")
            self.button.setEnabled(True)
            # Показываем ползунок громкости
            self.volume_slider.setVisible(True)
            logger.info("LoFi is now playing")

        elif state == QMediaPlayer.PlaybackState.StoppedState:
            self._on_stopped()

    def _on_error(self, error, error_string):
        logger.error(f"MediaPlayer error: {error_string}")
        self.button.setText("❌")
        self.is_loading = False
        self.is_playing = False
        self.button.setEnabled(True)
        # Скрываем ползунок при ошибке
        self.volume_slider.setVisible(False)

        QTimer.singleShot(2500, lambda: self.button.setText("🎵") if not self.is_playing else None)

    def _on_stopped(self):
        self.is_playing = False
        self.is_loading = False
        self.button.setText("🎵")
        self.button.setEnabled(True)
        # Скрываем ползунок громкости
        self.volume_slider.setVisible(False)

    def stop(self):
        """Вызывается при закрытии приложения"""
        if self.lofi_player:
            self.lofi_player.stop()
        self._on_stopped()

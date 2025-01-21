import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QListWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTime


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('music.ui', self)

        self.media_player = QMediaPlayer()
        self.playlist = []
        self.current_song_index = -1

        self.playlist_widget = self.findChild(QListWidget, 'playlist')

        self.playlist_widget.itemClicked.connect(self.item_selected)
        self.play.clicked.connect(self.play_music)
        self.pause.clicked.connect(self.pause_music)
        self.stop.clicked.connect(self.stop_music)
        self.previous.clicked.connect(self.previous_music)
        self.next.clicked.connect(self.next_music)
        self.load_songs_1.clicked.connect(self.load_songs)  # Connect load songs button

        # Volume Control
        self.volume.setValue(50)
        self.volume.valueChanged.connect(self.set_volume)

        # Seek Bar
        self.progresscontrol.sliderMoved.connect(self.set_position)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)

    def add_to_playlist(self, file_paths):
        for file_path in file_paths:
            self.playlist.append(file_path)
            self.playlist_widget.addItem(QListWidgetItem(file_path.split('/')[-1]))

    def load_songs(self):
        file_dialog = QtWidgets.QFileDialog(self, "Open Audio Files")
        file_dialog.setNameFilter("Audio Files (*.mp3);;All Files (*)")
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.add_to_playlist(selected_files)

    def item_selected(self, item):
        self.current_song_index = self.playlist_widget.row(item)
        self.play_music()

    def play_music(self):
        if self.current_song_index == -1 and self.playlist:
            self.current_song_index = 0

        if self.current_song_index >= 0:
            # Set media only if it's not already set
            if self.media_player.media() is None or self.media_player.currentMedia().canonicalUrl().toLocalFile() != \
                    self.playlist[self.current_song_index]:
                media_url = QUrl.fromLocalFile(self.playlist[self.current_song_index])
                self.media_player.setMedia(QMediaContent(media_url))


            self.media_player.play()

    def pause_music(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()  # Pause playback
        elif self.media_player.state() == QMediaPlayer.PausedState:
            self.media_player.play()
    def stop_music(self):
        self.media_player.stop()
        self.current_song_index = -1

    def previous_music(self):
        if self.current_song_index > 0:
            self.current_song_index -= 1
            self.play_music()

    def next_music(self):
        if self.current_song_index < len(self.playlist) - 1:
            self.current_song_index += 1
            self.play_music()

    def set_volume(self, value):
        self.media_player.setVolume(value)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def update_position(self, position):
        self.progresscontrol.setValue(position)
        current_time = QTime(0, 0, 0).addMSecs(position)
        duration = QTime(0, 0, 0).addMSecs(self.media_player.duration())

        if self.media_player.duration() > 0:
            self.labelTime.setText(current_time.toString("mm:ss") + " / " + duration.toString("mm:ss"))

    def update_duration(self, duration):
        if duration > 0:
            self.progresscontrol.setRange(0, duration)
        else:
            self.progresscontrol.setRange(0, 0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


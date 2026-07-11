import QtQuick

Rectangle {
    id: root
    objectName: "queueShellChrome"
    color: "#f6f3ed"
    implicitHeight: 88
    height: implicitHeight

    signal closeRequested

    property string titleText: queueShell ? queueShell.title : "Queue"
    property string subtitleText: queueShell ? queueShell.subtitle : ""

    Rectangle {
        anchors.fill: parent
        color: "#f6f3ed"

        Rectangle {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            height: 1
            color: "#d8d0c6"
        }

        Column {
            anchors.left: parent.left
            anchors.leftMargin: 24
            anchors.verticalCenter: parent.verticalCenter
            spacing: 4

            Text {
                text: root.titleText
                color: "#2f251d"
                font.pixelSize: 20
                font.bold: true
            }

            Text {
                text: root.subtitleText
                color: "#786b5e"
                font.pixelSize: 12
            }
        }

        Rectangle {
            anchors.right: parent.right
            anchors.rightMargin: 24
            anchors.verticalCenter: parent.verticalCenter
            width: 36
            height: 36
            radius: 18
            color: "#e7ddd0"

            Text {
                anchors.centerIn: parent
                text: "×"
                color: "#2f251d"
                font.pixelSize: 18
                font.bold: true
            }

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: root.closeRequested()
            }
        }
    }
}

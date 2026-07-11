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
            anchors.leftMargin: 20
            anchors.right: closeButton.left
            anchors.rightMargin: 16
            anchors.verticalCenter: parent.verticalCenter
            spacing: 4

            Text {
                width: parent.width
                text: root.titleText
                color: "#2f251d"
                font.pixelSize: 21
                font.weight: Font.DemiBold
                elide: Text.ElideRight
            }

            Text {
                width: parent.width
                text: root.subtitleText
                color: "#786b5e"
                font.pixelSize: 13
                wrapMode: Text.WordWrap
                maximumLineCount: 2
                elide: Text.ElideRight
            }
        }

        Rectangle {
            id: closeButton
            anchors.right: parent.right
            anchors.rightMargin: 16
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
                font.weight: Font.DemiBold
            }

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: root.closeRequested()
            }
        }
    }
}

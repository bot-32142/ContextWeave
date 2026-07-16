import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    objectName: "documentTranslationPaneChrome"
    color: "#f7f2ea"
    implicitHeight: 128

    signal polishToggled(bool enabled)
    signal translateRequested
    signal batchRequested

    property string tipText: translationPane ? translationPane.tip_text : ""
    property string polishLabelText: translationPane ? translationPane.polish_label : "Polish pass"
    property string translateLabelText: translationPane ? translationPane.translate_label : "Translate"
    property string batchLabelText: translationPane ? translationPane.batch_label : "Submit Batch Task"
    property string translateTooltipText: translationPane ? translationPane.translate_tooltip : ""
    property string batchTooltipText: translationPane ? translationPane.batch_tooltip : ""
    property string progressText: translationPane ? translationPane.progress_text : ""
    property bool polishEnabled: translationPane ? translationPane.polish_enabled : true
    property bool canTranslate: translationPane ? translationPane.can_translate : false
    property bool supportsBatch: translationPane ? translationPane.supports_batch : false
    property bool canBatch: translationPane ? translationPane.can_batch : false

    function buttonColor(enabled) {
        return enabled ? "#2f251d" : "#d7cebf"
    }

    function labelColor(enabled) {
        return enabled ? "#fcfaf6" : "#786b5e"
    }

    Column {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 10

        Text {
            width: parent.width
            text: root.tipText
            color: "#5f5447"
            font.pixelSize: 13
            wrapMode: Text.WordWrap
        }

        Text {
            width: parent.width
            text: root.progressText
            color: "#666666"
            font.pixelSize: 13
            wrapMode: Text.WordWrap
            visible: text.length > 0
        }

        Row {
            spacing: 8

            Rectangle {
                width: 150
                height: 38
                radius: 14
                color: root.polishEnabled ? "#c79c5d" : "#e6dccd"
                border.color: root.polishEnabled ? "#b3884c" : "#d0c4b4"
                border.width: 1

                Row {
                    anchors.centerIn: parent
                    spacing: 7

                    Rectangle {
                        anchors.verticalCenter: parent.verticalCenter
                        width: 12
                        height: 12
                        radius: 6
                        color: root.polishEnabled ? "#2f251d" : "#fffaf1"
                        border.color: "#8b765e"
                        border.width: 1
                    }

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: root.polishLabelText
                        color: "#2f251d"
                        font.pixelSize: 13
                        font.weight: root.polishEnabled ? Font.DemiBold : Font.Normal
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.polishToggled(!root.polishEnabled)
                }
            }

            Rectangle {
                width: 96
                height: 38
                radius: 14
                color: root.buttonColor(root.canTranslate)

                Text {
                    anchors.centerIn: parent
                    text: root.translateLabelText
                    color: root.labelColor(root.canTranslate)
                    font.pixelSize: 13
                    font.weight: Font.DemiBold
                }

                MouseArea {
                    id: translateMouseArea
                    anchors.fill: parent
                    enabled: root.canTranslate
                    cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
                    onClicked: root.translateRequested()
                }

                ToolTip.visible: translateMouseArea.containsMouse && !!root.translateTooltipText
                ToolTip.text: root.translateTooltipText
                ToolTip.delay: 500
            }

            Rectangle {
                visible: root.supportsBatch
                width: 156
                height: 38
                radius: 14
                color: root.canBatch ? "#fffaf1" : "#eee7dd"
                border.color: root.canBatch ? "#d0c4b4" : "#ddd4c8"
                border.width: 1

                Text {
                    anchors.centerIn: parent
                    text: root.batchLabelText
                    color: root.canBatch ? "#2f251d" : "#8b8174"
                    font.pixelSize: 13
                    font.weight: Font.DemiBold
                }

                MouseArea {
                    id: batchMouseArea
                    anchors.fill: parent
                    enabled: root.canBatch
                    cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
                    onClicked: root.batchRequested()
                }

                ToolTip.visible: batchMouseArea.containsMouse && !!root.batchTooltipText
                ToolTip.text: root.batchTooltipText
                ToolTip.delay: 500
            }
        }
    }
}

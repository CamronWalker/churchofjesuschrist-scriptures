<%*
const selection = tp.file.selection();
const modalForm = app.plugins.plugins.modalforms.api;
var result = await modalForm.openForm('Markup Selector');
if (result.status === 'cancelled') {
    console.log("cancelled");
    return; 
}
const markType = await result.asString('{{Type}}');
const colorSelector = await result.asString('{{Color Selector}}');
const includeFootnoteBoolean = await result.asString('{{Include Footnote}}');
const footnote = await result.asString('{{Footnote}}');
const lines = selection.split('\n');
const processedLines = lines.map(line => {
    const trimmed = line.trim();
    if (trimmed === '' || trimmed.startsWith('#')) {
        return line;
    } else {
        return `<span class="${markType}-${colorSelector}">${line}</span>`;
    }
});
const output = processedLines.join('\n');
tR += output;
if (includeFootnoteBoolean === "true") {
    if (footnote.trim() === '' || footnote === '{{Footnote}}') {
        tR += ' ^[]';
    } else {
        tR += ` ^[${footnote}]`;
    }
}
%>
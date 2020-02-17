export default function stringToHex(str) {
  return str
    .split("")
    .map(function(s) {
      return s.charCodeAt(0).toString(16);
    })
    .join("");
}

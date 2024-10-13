var fs = require('fs');
var parseMagicaVoxel = require('parse-magica-voxel');

fs.readFile("./bunny_small.vox", function (err, Buffer) {
  if (err) throw err;

  // MagicaVoxel 파일 파싱
  var voxelData = parseMagicaVoxel(Buffer);

  // JSON 파일로 저장
  fs.writeFile("voxel_data.json", JSON.stringify(voxelData, null, 2), function (err) {
    if (err) throw err;
    console.log("Voxel data saved to voxel_data.json");
  });
});
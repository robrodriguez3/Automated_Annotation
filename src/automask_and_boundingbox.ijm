dir=getDirectory("Choose a Directory ");
setBatchMode(true);

input = dir
output = dir

print("Got directory");

processFolder(input);

function processFolder(input){
	list = getFileList(input);
	for (i = 0; i < list.length; i++) {
		processFile(input, output, list[i]);
	}
}

function processFile(input, output, file) {
	print("Processing: " + input + file);
	open(input+file);
	Name=getTitle();
	Name=replace(Name,".jpg","");
	run("8-bit");
	print("Covert to 8-bit");
	setThreshold(100, 255);
	run("Convert to Mask");
	print("First threshold");
	run("Set Measurements...", "bounding redirect=None decimal=3");
	run("Analyze Particles...", "size=100-Infinity circularity=0.00-1.00 show=Masks display");
	saveAs("PNG", output+Name+"_mask.png");	
	selectWindow("Results");
	saveAs("Results", output+Name+".csv");
	run("Clear Results");
	close();
	print("Saved");
}

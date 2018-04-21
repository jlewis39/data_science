## INTRODUCTION TO DATA SCIENCE COURSE PROJECT WEBSITE (CS 341)

### TEAM NAME
A Team Has No Name

### DATA VISUALIZATION CHARTS
<html>
<head>

	<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.min.js"></script>
	<script type="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css"></script>
	<script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>

</head>


<body>

	<div class="container">
		<canvas id="myChart"></canvas>
	</div>

	<script>
		var myChart = document.getElementById('myChart').getContext('2d');
		$.ajax({url :'https://cors.io/?https://raw.githubusercontent.com/ateamhasnoname03/data_science/master/Data%20Integration%20and%20Analytics/output/task4_result.csv',
			async: false,

			 success: function(result){
			 	//console.log(data.responseText

				lines = result.split("\n") // split the values by the lines

				// convert the records to json values
				var records = lines.filter((s)=> s.length > 0).map((record) =>{
				
				details = record.match(/(".*?"|[^",]+)(?=\s*,|\s*$)/g)
				details = details || []
				return {name:details[0],address:details[1],avgRating:details[2],numPass:details[3],numCond:details[4],numFail:details[5]}
				
				})

				headers = records[0] // get the headers

				records.shift() // remove the first (headers) row

				var avgRatingValues = records.map((record) => record.avgRating)
				var passCounts = records.map((record) => record.numPass)
				var condCounts = records.map((record) => record.numCond)
				var failCounts = records.map((record) => record.numFail)

				var ratingToPass = records.map((record) => {
				var obj = {x:record.avgRating,y:record.numPass}
				return obj
				})

				var scatterChart = new Chart(myChart, {
			    type: 'scatter',
			    data: {
			        datasets: [{
			            label: '#Pass vs Average Review Rating',
			            data: ratingToPass,
			            backgroundColor: 'Green',
			            labels:['Label1']
			        }]
			    },
			    options: {
			        scales: {
			            xAxes: [{
			                type: 'linear',
			                position: 'bottom'
			            }]
			        }
			    }
				});	

			 }})
		
				
		
	</script>

</body>
</html>


### TEAM MEMBERS
- **Meghana Sanjay**
  < msanja3@uic.edu > 
  Meghana is a graduate student currently in her second semester at UIC. She's an energetic, enthusiastic, bubbly, jumpy, crazy sometimes lazy straight out of college girl and could dance before she learnt how to walk.
- **Joylyn Lewis**
  < jlewis39@uic.edu > 
  Joylyn is a graduate student in her first semester at UIC. She has over eight years of industry experience working as an SAP      consultant implementing ERP solutions. In her free time, she likes reading fiction, cooking and travelling.
- **Adarsh Hegde** < ahegde5@uic.edu >
  Adarsh is a graduate student in his second semester at UIC. He loves programming and football.
- **Stephen Walden** < swalde3@uic.edu >
  Stephen is an undergraduate student in his sixth semester at UIC. He started programming around computer games, and has started chasing a career in computer science. He has a year of experience working with Robotic Process Automation in the industry. He enjoys driving motorcycles and building with legos. [More about Stephen](https://walden1995.github.io/)

### WEEKLY STATUS REPORT
- The webpage for the Weekly Status Report is available [here](https://github.com/ateamhasnoname03/data_science/wiki/Weekly-Status-Report)
- The weekly status is also managed using the project board available [here](https://github.com/ateamhasnoname03/data_science/projects/1)



<!DOCTYPE html>
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
		
				
		console.log('Hello')
		/*var massPopChart = new Chart(myChart,{
			type:'bar', //bar, horizontal bar, pie, line, doughnuts, radar,polararea
			data:{
				labels:['Boston','Worcester','Springfield','Lowell','Cambridge', 'New Bedford'],
				datasets:[{
					label:'Population',
					data:[1002,1453,6564,2324,8521,2422],
					backgroundColor:'Orange'
				}]
			},
			options:{}
		});*/

	</script>

</body>
</html>

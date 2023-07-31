<?php

if (count($argv) >= 4) {
    $dir_name = $argv[1];
    $tmp_path = trim($argv[2],"'");
    $test_time = $argv[3];
    echo "bench.php (dir_name) (tmp_path) (test_time): $dir_name $tmp_path $test_time\n";
} else {
    print "bench.py error: dir_name tmp_path test_time";
    exit();
}

// Function to get the current timestamp in milliseconds
function getTimestampMillis()
{
    return round(microtime(true) * 1000);
}

// Function to perform the Sum of N Natural Numbers test
function sumOfNaturalNumbersTest()
{
    $n = 1000;
    $sum = 0;
    for ($i = 1; $i <= $n; $i++) {
        $sum += $i;
    }
}
function fancySumOfNaturalNumbersTest() {
    $n = 1000;
    $sum = array_sum(range(1, $n));
    return $sum;
}

// Function to perform the MD5 Hash Calculation test
function md5HashCalculationTest()
{
    $data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.";
    for ($i = 0; $i < 1000; $i++) {
        md5($data);
    }
}

// Function to perform the Random Number Generation test
function randomNumberGenerationTest()
{
    for ($i = 0; $i < 1000; $i++) {
        rand(0,100);
    }
}

// Function to perform the String Concatenation test
function stringConcatenationTest()
{
    $result = "";
    for ($i = 0; $i < 1000; $i++) {
        $result .= "Lorem ipsum dolor sit amet, ";
    }
}

// Function to perform the Matrix Multiplication test
function matrixMultiplicationTest()
{
    $size = 100; // Half the number of iterations compared to others
    $matrix1 = array();
    $matrix2 = array();
    $result = array();

    for ($i = 0; $i < $size; $i++) {
        for ($j = 0; $j < $size; $j++) {
            $matrix1[$i][$j] = $i + $j;
            $matrix2[$i][$j] = $i - $j;
            $result[$i][$j] = 0;
        }
    }

    for ($i = 0; $i < $size; $i++) {
        for ($j = 0; $j < $size; $j++) {
            for ($k = 0; $k < $size; $k++) {
                $result[$i][$j] += $matrix1[$i][$k] * $matrix2[$k][$j];
            }
        }
    }
}

// Function to perform the File I/O Operations test
function fileIOTest()
{
    global $tmp_path;
    $filePath = $tmp_path."php_benchmark_test.txt";
    $content = "f5*8sj!@%uKgP#T9Q&cA+d2^vhZ6bG9qU*rLMEnoV!xItTzNh%O^fqJjR&U*Lo8*mSdMvWJkTjz%hx9YypS3ecmqLnqehOM4vMK5nNvBXUzNz5#3QVy3K6u0Ad8p7xhWp2z9R0QiwzI0sXzCjaZrnojbfXnGf^&3M!J3+QGRM2FaZGkWi!PZJEM1bWVuDQb7PA5gJPd1#jn+X9QGv";

    $fileHandle = fopen($filePath, 'w');
    fwrite($fileHandle, $content);
    fclose($fileHandle);

    $fileHandle = fopen($filePath, 'r');
    fread($fileHandle, filesize($filePath));
    fclose($fileHandle);

    #unlink($filePath); #python doesn't why should we?
}

// Function to perform the Associative Array/Dictionary Manipulation test
function associativeArrayManipulationTest()
{
    $data = array(
        "one" => 1,
        "two" => 2,
        "three" => 3,
        "four" => 4,
        "five" => 5,
    );

    // Reverse the array
    $reversedData = array();
    $keys = array_keys($data);
    for ($i = count($keys) - 1; $i >= 0; $i--) {
        $reversedData[$keys[$i]] = $data[$keys[$i]];
    }

    // Sort the array (bubble sort)
    $sortedData = $data;
    $len = count($sortedData);
    for ($i = 0; $i < $len - 1; $i++) {
        for ($j = 0; $j < $len - $i - 1; $j++) {
            if ($sortedData[$keys[$j]] > $sortedData[$keys[$j + 1]]) {
                $temp = $sortedData[$keys[$j]];
                $sortedData[$keys[$j]] = $sortedData[$keys[$j + 1]];
                $sortedData[$keys[$j + 1]] = $temp;
            }
        }
    }
}

// Function to run the benchmarks for 30 seconds
function runBenchmark($testFunction)
{
    global $test_time;
    $startTime = getTimestampMillis();
    $endTime = $startTime + ($test_time*1000); # test duration


    $iterations = 0;
    while (getTimestampMillis() < $endTime) {
        $testFunction();
        $iterations++;
    }

    return $iterations;
}

// Run the benchmarks and save results to a file
$file = fopen("{$dir_name}/php_benchmark.txt", "w");

fwrite($file, "Sum of N Natural Numbers Test: " . runBenchmark("sumOfNaturalNumbersTest") . "\n");
fwrite($file, "Fancy Sum of N Natural Numbers Test: " . runBenchmark("fancySumOfNaturalNumbersTest") . "\n");
fwrite($file, "MD5 Hash Calculation Test: " . runBenchmark("md5HashCalculationTest") . "\n");
fwrite($file, "Random Number Generation Test: " . runBenchmark("randomNumberGenerationTest") . "\n");
fwrite($file, "String Concatenation Test: " . runBenchmark("stringConcatenationTest") . "\n");
fwrite($file, "Matrix Multiplication Test: " . runBenchmark("matrixMultiplicationTest") . "\n");
fwrite($file, "File I/O Operations Test: " . runBenchmark("fileIOTest") . "\n");
fwrite($file, "Associative Array Manipulation Test: " . runBenchmark("associativeArrayManipulationTest") . "\n");

fclose($file);

unlink($tmp_path."php_benchmark_test.txt");
?>

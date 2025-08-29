/*
Author       : Dreamguys
Template Name: Doccure - Bootstrap Template
Version      : 1.0
*/

(function($) {
    "use strict";

    // medicine Add More
    
    $(".medicine-info").on('click','.trash', function () {
        $(this).closest('.medicine-cont').remove();
        return false;
    });

    $(".add-medicine").on('click', function () {  
        
        var medicinecontent = '<div class="row form-row medicine-cont">' +
            '<div class="col-12 col-md-10 col-lg-11">' +
                '<div class="极row form-row">' +
                    '<div class="col-12 col-md-6 col-lg-3">' +
                        '<div class="form-group">' +
                            '<label>Medicine Name</label>' +
                            '<input type="text" name="medicine_name" class="form-control">' +
                        '</div>' +
                    '</div>' +
                    '<div class="col-12 col-md-6 col-lg-3">' +
                        '<div class="form-group">' +
                            '<label>Quantity</label>' +
                            '<input type="text" name="quantity" class="form-control">' +
                        '</div>' +
                    '</div>' +
                    '<div class="col-12 col-md-6 col-lg-3">' +
                        '<div class="form-group">' +
                            '<label>Frequency</label>' +
                            '<input type="text" name="frequency" class="form-control">' +
                        '</div>' +
                    '</div>' +
                    '<div class="col-12 col-md-6 col-lg-3">' +
                        '<div class="form-group">' +
                            '<label>Relation with meal</label>' +
                            '<input type="text" name="relation_with_meal" class="form-control">' +
                        '</div>' +
                    '</div>' +
                    '<div class="col-12 col-md-6 col-lg-6">' +
                        '<div class="form-group">' +
                            '<label>Duration</label>' +
                            '<input type="text" name="duration" class="form-control">' +
                        '</div>' +
                    '</div>' +
                    '<div class="col-12 col-md-6 col-lg-6">' +
                        '<div class="form-group">' +
                            '<label>Instruction</label>' +
                            '<input type="text" name="instruction" class="form-control">' +
                        '</div>' +
                    '</div>' +
                '</div>' +
            '</div>' +
            '<div class="col-12 col-md-2 col-lg-1"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
        '</div>';
        
        $(".medicine-info").append(medicinecontent);
        return false;
    });    
    
    
    // Test Add More

    $(".test-info").on('click','.trash', function () {
        $(this).closest('.test-cont').remove();
        return false;
    });

    $(".add-test").on('click', function () {  
        // Clone the first test-cont div (same method as report template)
        var $firstTest = $(".test-info .test-cont").first();
        if ($firstTest.length === 0) {
            // If no test-cont exists, create one manually (fallback)
            var testcontent = '<div class="row form-row test-cont">' +
                '<div class="col-12 col-md-10 col-lg-11">' +
                    '<div class="row form-row">' +
                        '<div class="col-12 col-md-5 col-lg-5">' +
                            '<div class="form-group">' +
                                '<label>Test Name</label>' +
                                '<select class="form-control test-name-select" name="test_name" onchange="updateTestId(this)">' +
                                    '<option value="">Select Test</option>';
            
            // Generate test options from testData
            if (typeof testData !== 'undefined' && testData.length > 0) {
                testData.forEach(function(test) {
                    testcontent += '<option value="' + test.test_id + '" data-test-id="' + test.test_id + '">' + test.test_name + '</option>';
                });
            }
            
            testcontent += '</select>' +
                            '</div>' +
                        '</div>' +
                        '<div class="col-12 col-md-6 col-lg-6">' +
                            '<div class="form-group">' +
                                '<label>Description</label>' +
                                '<input type="text" name="description" class="form-control">' +
                            '</div>' +
                        '</div>' +
                        '<div class="col-12 col-md-1 col-lg-1">' +
                            '<div class="form-group">' +
                                '<label>ID</label>' +
                                '<input type="number" name="id" class="form-control test-id-input" readonly>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="col-12 col-md-2 col-lg-1"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
            '</div>';
            
            $(".test-info").append(testcontent);
        } else {
            // Clone and reset values (same method as report template)
            var $clone = $firstTest.clone();
            $clone.find('select[name="test_name"]').val('');
            $clone.find('input[name="description"]').val('');
            $clone.find('.test-id-input').val('');
            $(".test-info").append($clone);
        }
        return false;
    });

    // Make updateTestId function globally available
    window.updateTestId = function(selectElement) {
        // Get the selected option
        const selectedOption = selectElement.options[selectElement.selectedIndex];
        // Get the test ID from data attribute
        const testId = selectedOption.getAttribute('data-test-id');
        // Find the closest test container
        const testContainer = selectElement.closest('.test-cont');
        // Find the ID input field within this container
        const idInput = testContainer.querySelector('.test-id-input');
        // Set the value
        if (idInput && testId) {
            idInput.value = testId;
        } else if (idInput) {
            idInput.value = '';
        }
    };

        
})(jQuery);

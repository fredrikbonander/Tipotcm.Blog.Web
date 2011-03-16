/**
 * Created by PAC.
 * User: broken
 * Date: 12/8/10
 * Time: 8:43 AM
 * To change this template use File | Settings | File Templates.
 */

ModelTest = TestCase('ModelTest');

ModelTest.prototype.testQueueSetToEmpty = function() {
    var isFalse = true,
        i = '',
        j = '';


    for (i in $.model.queue) {
        if ($.model.queue[i]) {
            for (j in $.model.queue[i]) {
                if ($.model.queue[i][j] && $.model.queue[i][j] !== false) {
                    isFalse = false;
                    break;
                }
            }
        }
    }

    assertEquals(true, isFalse);
};
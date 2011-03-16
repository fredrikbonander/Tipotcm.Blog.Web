/**
 * Created by .
 * User: broken
 * Date: 12/14/10
 * Time: 3:59 PM
 */

BridgeTestCase = TestCase('BridgeTest');

BridgeTestCase.prototype.setUp = function() {
    /*this.doc = document.createElement('div');

    var div = document.createElement('div'),
        input = document.createElement('input');

    div.id = 'python_js_bridge';
    input.type = 'hidden';
    input.id = 'language';
    input.value = 'se-sv';

    div.appendChild(input);
    this.doc.appendChild(div);
    document.appendChild(this.doc);*/

};

BridgeTestCase.prototype.testGetPropertyFromDOM = function() {
    /*:DOC += <div id="python_js_bridge"><input type="hidden" id="language" value="se-sv" /></div> */
    $.view.bridge.getValues();
    assertEquals('se-sv', $.view.bridge.properties.language);
};

dummyTestCase = TestCase('Dummy');
dummyTestCase.prototype.testTrue = function () {
    assertEquals('test', 'test');
};
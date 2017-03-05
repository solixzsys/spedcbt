<p>
                    {% for field in myfields %}
                         <div class="radio">
                        <label>
                            <input type="radio" name="optiongrp" />{{field}}
                        </label>
                    </div>
                    {% endfor %}
                </p>


                ***************************************************



                <p>

                    <div class="radio">
                        <label>
                            <input type="radio" name="optiongrp" />{{question.optionA}}
                        </label>
                    </div>

                    <div class="radio">
                        <label>
                            <input type="radio" name="optiongrp" />{{question.optionB}}
                        </label>
                    </div>

                    <div class="radio">
                        <label>
                            <input type="radio" name="optiongrp" />{{question.optionC}}
                        </label>
                    </div>

                    <div class="radio">
                        <label>
                            <input type="radio" name="optiongrp" />{{question.optionD}}
                        </label>
                    </div>

                </p>
                ************************************************************************
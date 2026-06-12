package nucleusteq.session3.java_training.model;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class User {
    private Long id;
    private String name;
    private Integer age;
    private String role;
}
